== WisBak - simple full/differential backup system ==
esj a-t w w d d-o-t c a

=== Features: ===
{{{
    * backup with GNU tar, through ssh for remote hosts
    * full and differential backups
    * keeps track of deleted files (through tar's snapshot files)
    * backs up to encrypted media
    * fully automatic media setup and detection
    * doesn't care if your backup media has a different device path every time
        (/dev/sdh one day, /dev/sdk the other)
    * support for exclude file to exclude files and directories
    * will not span filesystems (if you backup /home on host foo, and 
      /home/bob/remote_fs is an NFS-mounted remote directory, wisbak will
      not back it up, you must specify it as a separate backup target)
}}}

=== What's Missing: (where i want to go with this, and/or how you can help) ===
{{{
    * Restore GUI letting you browse your files, set a backup point in time to
      restore from, and restore files selectively
    * Fully automatic setup of backup server and remote hosts
    * Sanity check mode to check for potential problems before the backup
}}}

=== 5 Minutes Basic Setup: ===
{{{
    * get wisbak: in most cases, just do 'pip install wisbak'
    * install paramiko ('apt-get install python-paramiko' on ubuntu/debian)
    * setup a local user which will be the "backup user" - wisbak will ssh as
      that user to the remote hosts to do the backups (note that you STILL need
      to run wisbak as root!)
        * set that username in the connect_as param in wisbak.conf
    * make sure that user has ssh keys, normally that's done with 
          sudo -l -u BACKUP_USER ssh-keygen -t dsa
      (do NOT enter a passphrase, or if you do, you'll need to run wisbak under
       an ssh-agent)
    * distribute the ssh key to each host you'll want to backup (INCLUDING 
      localhost!), with:
          for h in HOST1 HOST2 ...; do
              sudo -l -u BACKUP_USER ssh-copy-id -i ~/.ssh/id_dsa.pub $h
          done
      (assuming you put the keys in the default place when running ssh-keygen)
    * edit wisbak.conf and set all the important parameters properly
    * copy wisbak.conf to /etc/default/wisbak.conf
    * insert a backup media; that should normally be a hard drive
    * THE ENTIRE CONTENTS OF THE BACKUP MEDIA WILL BE WIPED!!! YOU HAVE BEEN
      WARNED!!!!!!!!!!!!!!
    * run:
          dmesg |tail -50
      you should see something like:
          sd 18:0:0:0: [sdh] Attached SCSI disk
      remember the device name in between the brackets (sdh in this case)
    * run:
          sudo wisbak -a /dev/sdX
      replace sdX with the actual device name; note that once the drive has 
      been initialized, you won't have to care which device name it gets, and
      it doesn't matter if that changes in-between backup runs * wisbak will 
      find it.
    * wisbak will now repartition the drive, encrypt it, and format it; this 
      can take a while, especially for large USB-connected drives
    * wisbak will tell you to add the drive ID to its configuration file: 
      DO IT! If you don't, the drive will not be recognized.
    * to make the backup run daily, add a daily cron job like so:
          ./wisbak --cronscript
}}}

Your backup will run daily. Normally you'd run with 2 separate drives. When one
is full, or it's just been a while, insert the other one. Wisbak will do a full
backup again, as the media was swapped. To emulate other archivers / backupers
which will wipe an old tape that was re-inserted, add the '-d' option to
wisbak.

=== Restoring: ===
{{{
    To restore files for a given host/directory combination, mount the latest 
    backup media with:
        wisbak  -mv
    Then look into (by default) the wisbak directory in the mounted filesystem.
    Locate the LATEST level 0 backup (should look like
    wisbak-HOST-DIR-0-TIME.tgz if default configuration hasn't been
    changed) and cd to where you want to restore the file, and untar the backup
    with 
        tar xvzf PATH/TO/BACKUP_FILE.tgz --incremental
    Then find the LATEST level 1 backup, and untar it in the same place, with
    the same command. This will update files that were modified between the
    full and the differential backups, but will also create the files added,
    and delete those deleted.
}}}

**Run wisbak -h for runtime options.**

© Copyright 2010 Éric St-Jean, email: esj a-t w w d d-o-t c a

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


