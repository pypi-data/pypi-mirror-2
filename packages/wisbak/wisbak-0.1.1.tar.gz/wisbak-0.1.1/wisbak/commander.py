import fcntl
import logging
import os
import paramiko
import socket
import subprocess


class RunningCommand(object):
    stdin = None
    stdout = None
    stderr = None

    def __init__(self):
        pass

    def wait(self):
        pass

    def set_blocking(self, blocking, streams='all'):
        """Set blocking mode of associated i/o streams
        
        Set the stream to blocking (blocking=1, default) or nonblocking
        (blocking=0) of streams (which should be, e.g., (self.stdin,)), or
        'all' to set all of them.
        """
        pass

    def poll(self):
        """Checks if process is done"""
        pass

class PopenRunningCommand(RunningCommand):
    def __init__(self, process):

        super(PopenRunningCommand, self).__init__()

        self.process = process
        self.stdin = process.stdin
        self.stdout = process.stdout
        self.stderr = process.stderr

    def wait(self):
        return self.process.wait()

    def set_blocking(self, blocking, streams='all'):
        block = blocking and os.O_BLOCK or os.O_NONBLOCK
        if streams == 'all':
            streams = (self.stdin, self.stdout, self.stderr)
        for s in streams:
            fcntl.fcntl(s, fcntl.F_SETFL, block)

    def poll(self):
        return self.process.poll()

class ParamikoRunningCommand(RunningCommand):
    def __init__(self, stdin, stdout, stderr):

        super(ParamikoRunningCommand, self).__init__()

        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.channel = stdout.channel

    def wait(self):
        return self.channel.recv_exit_status()

    def set_blocking(self, blocking, streams='all'):
        # all streams are on the same channel
        block = blocking and 1 or 0
        self.channel.setblocking(block)
        
    def poll(self):
        return self.channel.exit_status_ready()

class CantConnectException(paramiko.PasswordRequiredException):
    pass

class ParamikoConnection(object):
    def __init__(self, host, username, commander):
        self.host = host
        self.username = username
        self.commander = commander

    def call_cmd(self, *args, **kwargs):
        return self.commander.call_cmd(*args, host=self.host, 
                                       runas=self.username, **kwargs)
    
    def close(self):
        self.commander.disconnect(host, username)

class Commander(object):
    """Call commands locally or through ssh, in the background"""
    connections = {}
    
    def __init__(self, logger=None):
        if logger:
            self.logger = logger
        else:
            logging.basicConfig()
            self.logger = logging.getLogger(__name__)
        self.agent = paramiko.Agent()

    def __del__(self):
        """Close all client connections when i'm deleted"""
        self.cleanup()

    def call_cmd(self, cmd, input=None, host=None, runas=None, 
                 waitoncmd=True, bufsize=-1, mightfail=False):
        """Calls cmd on host, re-using existing connections if available

        uses subprocess.Popen for local commands (host=None) and paramiko for
        remote command execution will automatically connect to remote host if
        there's no pre-existing connection.
        If waitoncmd is True, will wait for the cmd to finish, and will return
        stdout, stderr, return code. If False, it will return an object with
        stdin, stdout and stderr attributes, and a wait method to wait for the
        process to finish, returning the returncode.
        """
        if not host:
            assert runas == None # don't support it yet
            return self.call_local_cmd(cmd, input, waitoncmd, bufsize=bufsize,
                                       mightfail=mightfail)
        else:
            return self.call_remote_cmd(cmd, input, host, runas, waitoncmd, 
                                        bufsize=bufsize, mightfail=mightfail)

    def call_local_cmd(self, cmd, input=None, waitoncmd=True, bufsize=-1,
                       mightfail=False):
        self.logger.info('Calling local command: %s' % cmd)
        try:
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 bufsize=bufsize)
        except:
            self.logger.error("Can't execute %s:" % cmd)
            raise

        if waitoncmd:
            out, err = p.communicate(input)
            self.log_error(cmd, p.returncode, out, err, mightfail=mightfail)
            return out, err, p.returncode
        else:
            p.stdin.write(input)
            return RunningCommand(p)

    def call_remote_cmd(self, cmd, input=None, host=None, runas=None,
                        waitoncmd=True, bufsize=-1, mightfail=False):
        self.logger.info('Calling remote command on host %s as %s: %s' 
                         % (host, runas, cmd))
        try:
            client = self.connections[host][runas]['client']
        except KeyError:
            if runas:
                self.logger.info("Connecting to %s as %s"%(host, runas))
            else:
                self.logger.info("Connecting to " + host)
            if host not in self.connections:
                self.connections[host] = {}
            client = self._paramiko_connect(host, runas)
            self.connections[host][runas] = {
                'client': client,
                'commands': None
            }

        if not isinstance(cmd, (str, unicode)):
            cmd = ' '.join([e.replace(' ', '\ ') for e in cmd])
        stdin, stdout, stderr = client.exec_command(cmd, bufsize=bufsize)
        if input:
            stdin.write(input)
        
        if waitoncmd:
            out, err = stdout.read(), stderr.read()
            return_code = stdout.channel.recv_exit_status()
            self.log_error(cmd, return_code, out, err, mightfail=mightfail)

            return out, err, return_code
        else:
            return ParamikoRunningCommand(stdin, stdout, stderr)

    def cleanup(self):
        for host, username_conns in self.connections.iteritems():
            # username_conns is a dict keyed on "username connect as"
            for runas, connection in username_conns.iteritems():
                self.logger.debug('Closing %s@%s connection'%(runas, host))
                if connection['client']:
                    t = connection['client'].get_transport()
                    if t:
                        t.close()
                connection['client'].close()

    def connect(self, host, username=None):
        """SSH connect to host and returns an object which supports call_cmd
    
        Using the returned connection object, one can execute call_cmd without
        specifying host and runas everytime. The existing connection will be
        re-used as much as possible, but will re-connect if necessary.
        """
        if username:
            self.logger.info("Connecting to %s as %s"%(host, username))
        else:
            self.logger.info("Connecting to " + host)
        if host not in self.connections:
            self.connections[host] = {}
        client = self._paramiko_connect(host, username)
        self.connections[host][username] = {
            'client': client,
            'commands': None
        }
        return ParamikoConnection(host, username, self)

    def disconnect(self, host, username):
        """Close the username@host SSH connection"""
        client = self.connections[host][username]['client']
        client.close()
        del self.connections[host][username]
        
    def log_error(self, cmd, return_code, out, err, mightfail=False):
        if return_code and self.logger and not mightfail:
            msg = "Couldn't execute %s:\n%s"%(cmd, out+err)
            self.logger.error(msg)
            raise RuntimeError()
        else:
            msg = "%s:\n%s"%(cmd, out.strip() + err.strip())
            self.logger.info(msg)

    def _paramiko_connect(self, host, username=None):
        self.logger.info('Connecting through SSH to %s as %s'%(host, username))
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        # FIXME: this might be unnecessary, paramiko might find them anyways
        for k in (None, ) + self.agent.get_keys():
            # try first without an agent key, then with all the keys
            # the agent has, allowing usage of encrypted keys
            try:
                client.connect(host, username=username, pkey=k)
                break
            except paramiko.PasswordRequiredException:
                continue
            except (paramiko.SSHException, socket.gaierror) as e:
                raise CantConnectException(repr(e))
        else:
            # we're out of keys
            client.close()
            self.logger.debug("Ran out of keys trying to connect!")
            raise CantConnectException()
        return client


