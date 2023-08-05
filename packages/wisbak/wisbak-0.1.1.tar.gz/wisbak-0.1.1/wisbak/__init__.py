#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WisBak - simple full/differential backup system
See README.txt for information.

© Copyright 2010 Éric St-Jean, esj@wwd.ca

This file is part of WisBak.

    WisBak is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    WisBak is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with WisBak.  If not, see <http://www.gnu.org/licenses/>.
"""
import copy
import datetime as dt
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import fcntl
import glob
import logging
import os
import pwd
import re
import select
import smtplib
import sys
import tempfile
import time

import commander

# Global settings and options
# Don't modify unless you know what you're doing!!!
# directory on backup media where to put the backups
BACKUP_DIR = 'wisbak' 
# how we construct the backup file names
# keys are host, hashed_dir (where / is replaced by #), timetag, dir, level
# you *must* at least have host, (dir or hashed_dir) and timetag in there!
BACKUP_FN_FMT = 'wisbak-%(host)s-%(hashed_dir)s-%(level)s-%(timetag)s.tgz'
# format of log entries
# format keys: http://docs.python.org/library/logging.html#formatter-objects
LOG_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
# options to tar; we also use --gzip and --listed-incremental, so the client's
# tar must support those (most GNU tars should)
TAROPTS = ['--one-file-system', '--sparse', '--ignore-failed-read']
# format of timetag used
TIMETAG_FMT = '%Y%m%d-%H%M'

# paths on backup server
CONFIG_FILE = '/etc/default/wisbak.conf'
CRON_FILE = '/etc/cron.daily/wisbak.sh'
CRYPTSETUP = '/sbin/cryptsetup'
FDISK = '/sbin/fdisk'
LAST_BACKUP_FILE = 'last_backup' 
MKFS = "mkfs.ext3"
MOUNT = '/bin/mount'
SCSIINFO = 'scsiinfo'
SH = '/bin/sh'
SSH = '/usr/bin/ssh'
UMOUNT = '/bin/umount'
# paths on clients
# for now, you can't have per-client settings
SUDO = '/usr/bin/sudo'
TAR = '/bin/tar'

def is_mounted(path):
    """Checks in mtab if path is already mounted
    
    Returns mountpoint if so, None otherwise
    """
    mounts = [l.split() for l in open('/etc/mtab', 'r').readlines() 
              if l.startswith(path)]
    if mounts:
        return mounts[0][1]
    else:
        return None

class WisBak(object):
    def __init__(self, configfile=CONFIG_FILE, newdisk=None, 
                 yes=False, level0=False, mount=False, cron_script=False,
                 umount=False, delete_old=False):

        # save some parameters
        self.yes = yes
        self.configfile = configfile
        self.delete_old = delete_old
        self.newdisk = newdisk
        self.level0 = level0
        self.mount = mount
        self.cron_script = cron_script
        self.umount = umount
        self.l = logging.getLogger(self.__class__.__name__)
        
        # we also log to a file with level DEBUG so we have a detailed
        # report to email afterwards
        _, self.templog = tempfile.mkstemp()
        filehandler = logging.FileHandler(self.templog)
        formatter = logging.Formatter(LOG_FORMAT)
        filehandler.setFormatter(formatter)
        filehandler.setLevel(logging.DEBUG)
        root_logger = logging.getLogger()
        root_logger.addHandler(filehandler)
        self.summary = []

        # init commander instance
        self.commander = commander.Commander(logger=self.l)

        # read in configuration file
        self.read_conf()

        # if the config calls for appending to a global logfile, set it up
        if 'logfile' in self.conf and self.conf['logfile']:
            filehandler = logging.FileHandler(self.conf['logfile'])
            filehandler.setFormatter(formatter)
            filehandler.setLevel(logging.DEBUG)
            root_logger.addHandler(filehandler)
            self.l.info('Logging to ' + self.conf['logfile'])
        
        # we save the start time so we can tag everything with the same 
        # time
        self.start_time = dt.datetime.now()
        self.timetag = self.start_time.strftime(TIMETAG_FMT)

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        if 'commander' in self.__dict__:
            self.commander.cleanup()

    def backup(self, level=0):
        self.l.info("Backup start, level %d"%level)

        for h, disks in self.conf['backup_hosts']:
            for d in disks:
                try:
                    self._backup_host_disk(h, d, level)
                except commander.CantConnectException:
                    self.l.error((
                        u"Couldn't backup %(host)s: can't connect! "
                        u"Please check that you can connect to %(host)s as "
                        u"%(as)s from the local user %(user)s."
                    )%{'host': h, 'as':self.conf['connect_as'], 
                       'user': os.environ['USER']})
            self.l.info("Done with " + h)
        self.l.info("Done with all hosts.")
    
    def _backup_host_disk(self, host, disk, level):
        username = self.conf.get('connect_as', None)

        # do this for every disk to backup on every host
        self.l.info("Backing up %s on %s"%(disk, host))

        path_args = {'host': host, 'dir':disk, 'timetag': self.timetag,
                     'hashed_dir':disk.replace('/','#'), 
                     'level':level}

        conn = self.commander.connect(host, username)

        # if we're doing a level 1+ backup, is there actually a
        # full backup done already for this host+dir?
        if level > 0:
            path_args_copy = copy.copy(path_args)
            path_args_copy['level'] = 0
            path_args_copy['timetag']='*'
            base_fn = BACKUP_FN_FMT%path_args_copy
            backup_file_fn = os.path.join(self.backup_dir, base_fn)
            if not glob.glob(backup_file_fn):
                self.l.warn(
                    (u"Level %d backup requested, but no prior "
                     u"full backup exists. Switching to full backup.") 
                    % path_args['level']
                )
                path_args['level'] = 0

        # snapshot file handling
        snap_file = self.conf['snap_file']%path_args
        o, e, rc = conn.call_cmd(['test',  '-f', snap_file], mightfail=True)
        if rc == 0: # there's a snapshot file for this host+dir
            if path_args['level'] == 0:
                # full backup: empty snapshot file
                o, e, rc = conn.call_cmd(['rm', '-f', snap_file])
            else:
                # diff backup: copy the snapshot file to a safe loc'n
                o, e, rc = conn.call_cmd('tempfile')
                snap_temp = o.strip()
                o, e, rc = conn.call_cmd(['cp', snap_file, snap_temp])
        else:
            # there's no snapshot file, this will have to be a 
            # level 0 backup
            if path_args['level'] > 0:
                self.l.warn(
                    (u"Level %d backup requested, but no prior "
                     u"snapshot file exists on destination. Switching "
                     u"to full backup.") % level
                )
                path_args['level'] = 0
        
        # full path to exclude file on remote host
        exclude_from = self.conf['exclude_file']%path_args

        # check if exclude file exists on remote host
        o, e, rc = conn.call_cmd(['test', '-f', exclude_from], mightfail=True)
        exclude = (rc == 0) and ['-X', exclude_from] or []

        tar_cmd = ([SUDO, TAR, 'czf', '-'] 
                   + ['--listed-incremental=' + snap_file] 
                   + exclude + TAROPTS 
                   + [disk, ])

        # open backup file
        base_fn = BACKUP_FN_FMT%path_args
        backup_file_fn = os.path.join(self.backup_dir, base_fn)
        backup_file = open(backup_file_fn, 'w')

        # START BACKUP
        self.l.warn((u"Connecting to %s and backing up %s "
                     u"(this may take a while)")%(host, disk))
        start_time = time.time()
        p = conn.call_cmd(tar_cmd, waitoncmd=False, bufsize=10000000)

        # FIXME: abstract paramiko from this
        while not p.poll():
            r, w, x = select.select([p.channel,], [], [])
            if p.channel.recv_stderr_ready():
                err = p.channel.recv_stderr(1024)
                if len(err) == 0:
                    break
                self.l.warn("%s(%s):%s"%(host, disk, err))
            if p.channel.recv_ready():
                data = p.channel.recv(1024)
                if len(data) == 0:
                    break
                backup_file.write(data)
        total_time = time.time() - start_time
        
        # read any trailing data that happened between the last
        # read and the time the process ended
        if p.channel.recv_stderr_ready():
            err = p.channel.recv_stderr(1000).strip()
            self.l.warn("%s(%s):%s"%(host, disk, err))
        if p.channel.recv_ready():
            backup_file.write(p.channel.recv(1000000))

        backup_size = backup_file.tell()
        backup_file.close()

        # DONE BACKUP

        if p.wait():
            self.l.error("Error trying to backup %s on %s"%(disk, host))
        else:
            self.l.info("Done backing up %s on %s, total %d bytes"
                        %(disk, host, os.stat(backup_file_fn).st_size))

        if path_args['level'] > 0:
            # move the old snapshot file back
            # otherwise will will always be incremental
            conn.call_cmd( ['mv', snap_temp, snap_file])
        msg = (
            "Backup of %(host)s:%(dir)s "%path_args
            + "completed in %dm%ds. "%(total_time//60, total_time%60)
            + "There were %serrors. "%('' if p.wait() else 'no ')
            + "Compressed backup size is %.1f MiB. "%(backup_size/1024**2)
            + "Average speed of %.1f MB/s."%(backup_size/1e6/total_time)
        )
        self.summary.append(msg)
        self.l.warn(msg)
            
        self.l.info("Done with %s:%s" % (host, disk))

    def check_runtime_dir(self):
        """Creates the runtime directory if not present"""
        if not os.path.isdir(self.conf['runtime_data']):
            os.mkdir(self.conf['runtime_data'])

    def config_newdisk(self):
        """Re-partitions drive and encrypts the partition, ready for backups"""
        if (self.conf['key'] == 'CHANGEME'
            or len(self.conf['key']) < 10):
            self.l.error("Please change the key to a random string "
                         "at least 10 characters long in " + self.configfile)
            raise RuntimeError("Bad encryption key")
    
        disk_serial, err, rc = self.commander.call_cmd(
            [SCSIINFO, '-s', self.newdisk]
        )
        disk_info, err, rc = self.commander.call_cmd(
            [FDISK, '-l', self.newdisk]
        )
        self.l.warn("About to OBLITERATE " + self.newdisk)
        self.l.warn(disk_serial)
        self.l.warn(disk_info)
        if not self.yes:
            sys.stderr.write("##DANGER##" * 8 + '\n')
            sys.stderr.write("##DANGER##" * 8 + '\n')
            sys.stderr.write("##DANGER##" * 8 + '\n')
            sys.stderr.write(disk_info + disk_serial)
            sys.stderr.write(
                (u"You're about to COMPLETELY NUKE THIS DRIVE: %s\n"
                 u"ARE YOU SURE???\n"
                 u"Type yes in uppercase to continue: ")%self.newdisk
            )
            answer = raw_input()
            if answer != 'YES':
                self.l.error("Aborted.")
                raise RuntimeError("Aborted.")

        # create a new partition table with 1 partition covering the whole
        # disk
        self.l.info("Creating new partition table")
        cmd = [FDISK, self.newdisk]
        self.commander.call_cmd(cmd, 'o\nn\np\n1\n\n\nw\n')
        newpart = self.newdisk + '1'

        # now LUKS-format it with the configured passphrase
        self.l.info("luksFormat-ing the new partition with the configured key")
        cmd = [CRYPTSETUP, '-q', 'luksFormat', newpart]
        self.commander.call_cmd(cmd, self.conf['key']+'\n')

        # find out the UUID for the new partition
        blk_id, err, rc = self.commander.call_cmd(['blkid', newpart])
        match = re.compile('[/\w]+:.*UUID="(?P<uuid>[-\w]+)".*').match(blk_id)
        if not match:
            self.l.error("Couldn't find block UUID for " + newpart)
            raise RuntimeError()
        blk_id = match.groupdict()['uuid']
        self.l.warn("New partition has UUID " + blk_id)

        # format the new partition
        self.l.info("Unlocking " + newpart)
        cmd = [CRYPTSETUP, 'luksOpen', newpart, blk_id]
        self.commander.call_cmd(cmd, self.conf['key']+'\n')
        crypt_disk = os.path.join('/dev/mapper', blk_id)
        self.l.info("Formatting " + crypt_disk + " (this may take a while)")
        self.commander.call_cmd([MKFS, '-q', crypt_disk])
        
        # luksClose it, we're done
        self.l.info("Locking partition back")
        time.sleep(2) # for some reason, something keeps it busy after mkfs
        self.commander.call_cmd([CRYPTSETUP, 'luksClose', blk_id])
    
        self.l.warn("Done.IMPORTANT: Please add %s to disks in %s"
                    %(blk_id, self.configfile))
        self.l.warn("This disk will not be used UNTIL YOU DO SO.")

    def delete_old_backups(self):
        """Delete old backups from backup media, for media rotation
        
        Like tape archivers do.
        """
        self.l.warn("Deleting old backups from %s!!!" % self.backup_dir)
        self.l.warn("Press ctrl-c within 10 seconds to abort.")
        time.sleep(10)
        for f in os.listdir(self.backup_dir):
            full = os.path.join(self.backup_dir, f)
            self.l.info('Deleting ' + full)
            os.remove(full)

    def email_report(self):
        fromaddr = self.conf.get('from_email', None)
        toaddr = self.conf.get('admin_email', None)

        if not toaddr:
            self.l.info("No one to email report to")
        else:
            self.l.info("Emailing report to " + toaddr)
            title = "Backup report %s"%self.start_time.ctime()
            msg = MIMEMultipart()
            msg['Subject'] = Header(title, 'utf-8')
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg.attach(
                MIMEText("%s\n\nBackup Summary:\n%s\n\nDetailed log attached."
                         %(title, '\n'.join(self.summary)))
            )
            msg.attach(MIMEText(open(self.templog, 'r').read()))
            smtp_conf = self.conf.get('smtp_server', {'host':'localhost'})
            if not smtp_conf.get('use_ssl', False):
                SMTP = smtplib.SMTP
            else:
                SMTP = smtplib.SMTP_SSL
            s = SMTP(smtp_conf['host'], smtp_conf.get('port', 25))
            if smtp_conf.get('use_tls', False):
                s.starttls()
            if smtp_conf.get('username', None):
                s.login(smtp_conf['username'], smtp_conf.get('password', ''))
            s.sendmail(fromaddr, toaddr, msg.as_string())
            s.quit()

    def find_backup_disks(self):
        self.l.info("Finding attached backup disks")

        # find UUIDs for all plugged-in disks
        alldisks = [os.path.basename(d) 
                    for d in glob.glob('/dev/disk/by-uuid/*')]

        # intersect with the list of backup disks
        pluggedin = set(alldisks).intersection(self.conf['disks'])
        if not pluggedin:
            self.l.error("No backup disk is plugged-in, aborting.")
            raise RuntimeError("No backup disk plugged in.")
        
        # get the first one if >1
        self.disk_uuid = pluggedin.pop()
        self.disk = os.path.join('/dev/disk/by-uuid', self.disk_uuid)
        if pluggedin:
            self.l.warning("More than 1 backup disk are plugged-in, using "
                           + self.diskuuid)

        # find out where it's mounted if it is
        crypt_disk = os.path.join('/dev/mapper', self.disk_uuid)
        self.mountpt = is_mounted(crypt_disk)

        self.l.info('Backups will go to '+self.disk)

    def go(self):
        try:
            self._go()
        except:
            self.cleanup()
            raise
        self.cleanup()

    def _go(self):
        locked_pid = self.lock()
        if self.lock():
            msg = ("Can't acquire lock - another backup operation is "
                   "currently under way (pid %d)")%locked_pid
            self.l.error(msg)
            raise RuntimeError(msg)
        if self.newdisk:
            self.config_newdisk()
        elif self.mount:
            self.find_backup_disks()
            self.mount_backup_disk()
            print "\nBackup media is mounted on %s\n"%self.mountpt
        elif self.umount:
            self.find_backup_disks()
            # mounting it will do nothing
            self.mount_backup_disk()
            self.umount_backup_disk()
            print "\nBackup media is now unmounted and can be removed.\n"
        elif self.cron_script:
            self.setup_cron_script()
        else:
            self.find_backup_disks()
            self.mount_backup_disk()
            self.new_media = self.is_new_backup_media()
            level = 0 if (self.level0 or self.new_media) else 1
            if self.delete_old and self.new_media:
                self.delete_old_backups()
            if self.level0:
                self.l.warn("Backup level 0 forced")
            self.backup(level)
            self.is_new_backup_media(update=True)
            try:
                self.umount_backup_disk()
            except RuntimeError:
                # we don't want to stop if we couldn't unmount
                self.l.error("Couldn't unmount the drive after backup. "
                             "Do not remove it before unmounting and "
                             "unlocking it first!")
            total_time = (dt.datetime.now() - self.start_time).seconds
            msg = "WisBak completed in %dm%ds."%(total_time//60, total_time%60)
            self.summary.append(msg)
            self.l.info(msg)
            self.email_report()
        self.lock(unlock=True)

    def is_new_backup_media(self, update=False):
        """Checks if backup media is different than last one used
        
        If update, then update the backup file to remember this backup."""
        self.check_runtime_dir()
        last_file = os.path.join(self.conf['runtime_data'], LAST_BACKUP_FILE)
        if update:
            return open(last_file, 'w').write(self.timetag)
        is_new = False
        if not os.path.exists(last_file):
            is_new = True
        else:
            last_time = open(last_file, 'r').read().strip()
            expected_files = BACKUP_FN_FMT%{'host':'*', 'hashed_dir':'*', 
                                            'dir':'*', 'timetag':last_time,
                                            'level':'*'}
            is_new = (last_time
                      and not glob.glob(os.path.join(self.backup_dir, 
                                                     expected_files)))
        if not is_new:
            self.l.debug("The same backup media as last time was detected.")
        else:
            self.l.warn("New backup media detected!")
        return is_new

    def lock(self, unlock=False):
        """Get a lock, to make sure another backup operation isn't running
        
        Returns 0 if lock acquired, or the PID of the process who has it
        it not. If unlock, then the lock is released instead.
        """
        self.check_runtime_dir()
        lock_file_fn = os.path.join(self.conf['runtime_data'], 'wisbak.pid')
        self.lock_file = open(lock_file_fn, 'a+')
        if unlock==True:
            fcntl.lockf(self.lock_file, fcntl.LOCK_UN)
            self.lock_file.close()
            os.unlink(lock_file_fn)
        else:
            try:
                fcntl.lockf(self.lock_file, fcntl.LOCK_EX|fcntl.LOCK_NB)
            except IOError:
                pid = int(self.lock_file.read())
                self.lock_file.close()
                return pid
                
            # lock acquired
            self.lock_file.truncate()
            self.lock_file.write('%s'%os.getpid())
            self.lock_file.flush()
            return 0

    def unlock(self):
        self.lock(unlock=True)

    def mount_backup_disk(self):
        self.l.info("Unlocking " + self.disk)

        crypt_disk = os.path.join('/dev/mapper', self.disk_uuid)
        if os.path.exists(crypt_disk):
            self.l.info("%s already unlocked to %s"%(self.disk, crypt_disk))
        else:
            self.commander.call_cmd(
                [CRYPTSETUP, 'luksOpen', self.disk, self.disk_uuid], 
                self.conf['key']+'\n'
            )

        self.mountpt = is_mounted(crypt_disk)
        if self.mountpt:
            self.l.info("%s already mounted on %s"%(crypt_disk, self.mountpt))
        else:
            self.mountpt = tempfile.mkdtemp()
            self.l.info("Mounting " + crypt_disk)
            self.commander.call_cmd([MOUNT, crypt_disk, self.mountpt])
        self.backup_dir = os.path.join(self.mountpt, BACKUP_DIR)
        if not os.path.isdir(self.backup_dir):
            self.l.info("Creating backup directory " + self.backup_dir)
            os.mkdir(self.backup_dir)

    def read_conf(self):
        self.l.warn("Reading config from " + self.configfile)
        if not os.path.exists(self.configfile):
            src_conf = os.path.join(
                os.path.abspath(
                    os.path.dirname(__file__)
                ), 'wisbak.conf'
            )
            self.l.warn("%s doesn't exist!!! Using %s instead."
                        % (self.configfile, src_conf))
            self.configfile = src_conf
        self.conf = {}
        execfile(self.configfile, globals(), self.conf)
        conf_copy = copy.copy(self.conf)
        conf_copy['key'] = '***'
        self.l.debug("Read: %s"%conf_copy)

    def setup_cron_script(self):
        self.l.info("Creating daily cron script in " + CRON_FILE)
        open(CRON_FILE, 'w').write(
            u"#!/bin/sh\n"
            u"%s -qf %s\n"%(os.path.abspath(sys.argv[0]),
                           CONFIG_FILE))
        os.chmod(CRON_FILE, 0o755)

    def umount_backup_disk(self):
        self.l.info("Unmounting "+self.mountpt)
        self.commander.call_cmd([UMOUNT, self.mountpt])
        os.rmdir(self.mountpt)

        self.l.info("Locking "+self.disk)
        self.commander.call_cmd([CRYPTSETUP, 'luksClose', self.disk_uuid])


