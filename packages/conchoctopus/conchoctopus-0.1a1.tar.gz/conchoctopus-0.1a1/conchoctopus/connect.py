#!/usr/bin/env python
"""
Simplified conch client API.
"""


from twisted.internet import defer, protocol, reactor, threads
from twisted.conch.error import ConchError
from twisted.conch.client import default, options
from twisted.conch.client.knownhosts import KnownHostsFile
from twisted.conch.ssh import connection, transport, channel, common
from twisted.conch.ssh.keys import Key, EncryptedKeyError
from twisted.python import log
from twisted.python.filepath import FilePath

import struct
from os import getenv
from os.path import expanduser

class Error(Exception):
    """
    General errors coming from this module.
    """



class ConchServerError(ConchError):
    """
    Errors that comes from server.
    """



class CommandOutput:
    """
    Represents command's output.

    @ivar stdout: data from command's standard output
    @type stdout: C{str}/C{None} if not set
    
    @ivar stderr: command's standard error
    @type stderr: C{str}/C{None} if not set
     
    @ivar exit_code: command's exit code
    @type exit_code: C{str}/C{None} if not set

    """
    def __init__(self, command, exit_code=None, stdout=None, stderr=None):
        self.command = command
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr


    def __repr__(self):
        msg='%r command run ' % self.command
        if self.exit_code == 0:
            msg+='succesfully'
        else:
            msg+='failed'
        msg+=', exit code: %r, stdout:%r, stderr:%r' % (self.exit_code, self.stdout, self.stderr)
        return msg



class CommandError(Error):
    """
    Returned when command failed.

    @ivar output: C{CommandOutput} of failed command
    @ivar finishedCommands: C{list} of C{CommandOutput} 
                            that executed successfully
    """
    def __init__(self, output, finishedCommands=None):
        self.output = output
        self.finishedCommands = finishedCommands



class ExecCmdChannel(channel.SSHChannel):
    """
    Channel used to execute command and gather its output.
    Run factory methods commandSuccess or commandFailed 
    with C{CommandOutput} and corresponding deferred as
    an arguments depending on command's success or failure.
    
    @ivar name: name of this channel, always set to 'session'
    @type name: C{str}
    
    @ivar channel_type: type of this channel, always set to 'exec'
    @type channel_type: C{str}
    
    @ivar cmd: command to execute
    @type cmd: C{str}

    @ivar deferred: command's deferred that gets passed to the factory
                    when command has been executed
    @type deferred: C{defer.Deferred}

    @ivar output: command's output
    @type output: C{CommandOutput}
    """
    name = 'session'
    channel_type = 'exec'
    factory = None


    def __init__(self, command, deferred, *args):
        channel.SSHChannel.__init__(self, *args)
        self.command = command
        self.deferred = deferred
        self.output = CommandOutput(command)


    def cmdSent(self, ignored):
        self.conn.sendEOF(self)


    def channelOpen(self, ignoredData):
        """
        Execute command, errback on error.
        """
        log.msg('Channel opened')
        d = self.conn.sendRequest(self, self.channel_type, common.NS(self.command), wantReply = 1)
        d.addCallback(self.cmdSent)
        d.addErrback(lambda reason: self.factory.errorReceived(ConchError(reason.value.value, 
                                                                         'Channel request was: %r %r' % 
                                                                         (self.channel_type, self.command))))


    def openFailed(self, reason):
        """
        Can't open channel.Errback with reason why.
        """
        self.factory.errorReceived(ConchError(reason.value, 'Channel open failed.'))


    def dataReceived(self, data):
        """
        Received new data.Just add it to a buffer.
        """
        log.msg('Received data %r' % data)
        if self.output.stdout is None:
            self.output.stdout = ''
        self.output.stdout += data


    def extReceived(self, dataType, data):
        """
        Received extended data.Check if it's standard error
        and add it to buffer.Log unknown data type.
        """
        if dataType == connection.EXTENDED_DATA_STDERR:
            if self.output.stderr is None:
                self.output.stderr = ''
            self.output.stderr += data
        else:
            log.msg('Received unknown data type %r' % dataType)


    def request_exit_status(self, s):
        """
        Received command's exit status.Convert and then store it.
        """
        self.output.exit_code = struct.unpack('>l', s)[0]
        log.msg('Received exit status: %d' % self.output.exit_code)


    def closed(self):
        """
        Channel has been closed.
        """
        log.msg('Channel closed')
        if self.output.exit_code != 0:
            self.factory.commandFailed(self.output, self.deferred)
        elif self.output.exit_code == None:
            self.factory.errorReceived(ConchError(self.output, "Haven't received exit code"))
        else:
            self.factory.commandSuccess(self.output, self.deferred)



class SSHClientConnection(connection.SSHConnection):
    """
    This class is used by factory to manage channel execution.
    """
    factory=None


    def serviceStarted(self):
        """
        Run first available command.
        """
        self.factory.runNextCommand()


    def loseConnection(self):
        """
        Close connection.
        """
        self.transport.transport.loseConnection()



class SSHUserAuthClient(default.SSHUserAuthClient):
    """
    Authenticate using password or SSHAgent.
    
    @ivar password: password used for authentication
    @type password: C{None} if not in use/C{str}

    @ivar tried: true when password is used first time 
    @type tried: C{bool}
    """
    password = None
    tried = False


    def tryAuth(self, auth_method):
        """
        Check if user wants to authenticate
        with given method.
        """
        if auth_method not in self.factory.config_opts['auth_methods']:
            log.msg("%r not allowed as an authentication method." % auth_method)
            return False
        return default.SSHUserAuthClient.tryAuth(self, auth_method)


    def _getPassword(self, prompt):
        """
        We don't support interactive password
        prompts.
        """
        return None
    

    def getPrivateKey(self):
        """
        If key is encrypted give up.
        """
        try:
            return default.SSHUserAuthClient.getPrivateKey(self)
        except EncryptedKeyError, e:
            log.msg("%r is password encrypted key which I don't directly support."
                    "You can add it to ssh-agent and then try again." % self.usedFiles[-1])
            return None


    def getPassword(self, prompt = None):
        """
        Authenticate with password.
        """
        # try just once
        if self.tried:
            return None
        else:
            self.tried = True
        if self.password is None:
            return None
        try:
            return defer.succeed(self.password)
        except AttributeError:
            return None



SSH_DISCONNECT = [ 0,
  'HOST_NOT_ALLOWED_TO_CONNECT',             
  'PROTOCOL_ERROR',                          
  'KEY_EXCHANGE_FAILED',                     
  'RESERVED',
  'MAC_ERROR',
  'COMPRESSION_ERROR',
  'SERVICE_NOT_AVAILABLE',
  'PROTOCOL_VERSION_NOT_SUPPORTED',
  'HOST_KEY_NOT_VERIFIABLE',
  'CONNECTION_LOST',
  'BY_APPLICATION',
  'TOO_MANY_CONNECTIONS',
  'AUTH_CANCELLED_BY_USER',
  'NO_MORE_AUTH_METHODS_AVAILABLE',
  'ILLEGAL_USER_NAME']



class SSHClientTransport(transport.SSHClientTransport):
    """
    Transport that verify server's key, handle client's disconnect
    messages and server's errors.
    """


    def verifyHostKey(self, hostKey, ignored):
        """
        Check if server's key is known.A new key can be added to
        known_hosts without verification when relevant option is set by a user.
        """
        self.knownHosts = KnownHostsFile.fromPath(FilePath(self.factory.config_opts['known_hosts']))
        class UI(object):
            def prompt(self, text):
                if self.factory.config_opts['known_hosts_autoaddnew']:
                    log.msg('yes')
                    return defer.succeed(True)
                else:
                    log.msg('no')
                    return defer.succeed(False)
        peerAddr=self.transport.getPeer().host
        def verify(hostname, failure=None):
            if failure:
                log.msg("Can't resolve hostname %s: %s" % (hostname, failure))
            ui=UI()
            ui.factory=self.factory
            d=self.knownHosts.verifyHostKey(ui, peerAddr, hostname, Key.fromString(hostKey)) 
            def _cbErr(f):
                self.factory.errorReceived(f)
                self.transport.loseConnection()
            d.addErrback(_cbErr)
        def gethostbyaddr(addr):
            import socket
            return socket.gethostbyaddr(addr)[0]
        hname = threads.deferToThread(gethostbyaddr, peerAddr)
        hname.addCallback(verify)
        hname.addErrback(lambda failure: verify(peerAddr, failure))
        return hname


    def connectionSecure(self):
        """
        Run user authentication service.
        """
        log.msg('Server version string: %s' % self.otherVersionString)
        self.requestService(self.factory.userAuth)


    def _reasonCodeToSym(self, reasonCode):
        """
        Returns symbolic representation of
        disconnect error code.
        """
        try:
            sname = SSH_DISCONNECT[reasonCode]
        except IndexError:
            sname = reasonCode
        return sname


    # According to rfc4253 not all of the disconnect messages
    # are errors.Shall we errback only on specific type of messages?
    def receiveError(self, reasonCode, desc):
        """
        Covert error code to symbol and errback with error messages.
        """
        sname = self._reasonCodeToSym(reasonCode)
        log.msg('Received SSH_DISCONNECT_%s description=%s' % (sname, desc))
        self.factory.errorReceived(ConchServerError(sname, desc))


    def sendDisconnect(self, reasonCode, desc):
        """
        Covert error code to symbol and errback with error messages.
        """
        transport.SSHClientTransport.sendDisconnect(self, reasonCode, desc)
        self.factory.errorReceived(ConchError(self._reasonCodeToSym(reasonCode), desc))


    def connectionLost(self, reason):
        """
        Log reason why connection was lost.
        """
        transport.SSHClientTransport.connectionLost(self, reason)
        log.msg('Connection lost %s' % reason.value)



default_config_opts={'known_hosts': expanduser('~/.ssh/known_hosts'), 
                     'known_hosts_autoaddnew': False,
                     'auth_methods': ['publickey', 'password'],
                     'auth_keys': ['~/.ssh/id_rsa', '~/.ssh/id_dsa'],
                     'auth_useagent': True}



class SSHClientFactory(protocol.ClientFactory):
    """
    @ivar finalDeferred: deferred fired when all channels
                         has been executed or when error occured
    @type finalDeferred: C{Deferred}

    @ivar user: user used for authentication
    @type user: C{str} 

    @ivar connection: instance of C{SSHClientConnection} subclass used to
                      establish connection between us and a server 
                      and managing channel execution
    @type connection: instance of C{SSHClientConnection} subclass
    
    @ivar userAuth: class responsible for user authentication
    @type userAuth: C{SSHUserAuthClient} class

    @ivar transport: class that handles low level protocol details 
    @type transport: C{SSHClientTransport}
    
    @ivar config_opts: configuration variables used to control client's
                       behaviour
    @type config_opts: C{dict}

    @ivar user: user name used for authentication
    @type user: C{str} or C{None} if not set

    @ivar host: host name used for connection
    @type host: C{str} or C{None} if not set
    """

    def __init__(self, finalDeferred, user, connection, userAuth=SSHUserAuthClient, 
                 transport=SSHClientTransport, config_opts=default_config_opts):
    
        self.protocol = transport
        self.connection = connection()
        o=options.ConchOptions()
        if config_opts['auth_useagent']:
            o['noagent'] = False
        else:
            o['noagent'] = True
        self.userAuth = userAuth(user, o, self.connection)
        self.userAuth.options.identitys = config_opts['auth_keys']
        # On every level in stack, we keep
        # reference back to factory to allow
        # for consistent error handling
        self.connection.factory = self
        self.userAuth.factory = self      
        self.config_opts = config_opts
        # Used for return outputs
        self.finalDeferred = finalDeferred

        self.user = user
        self.host = None



class SSHExecCmd(SSHClientFactory):
    """
    Factory used to glue togther various library components.

    @ivar commands: List of commands to execute
    @type commands: C{list} of C{str}
    
    @ivar commandsDeferreds: Deferreds used to callback with C{CommandOutput} 
                             or errback with C{CommandError} as an 
                             argument depending on command's exit code 
                             (see C{ExecCmdChannel for details).
    @type commandsDeferreds: C{list} of C{defer.Deferred}

    @ivar finalDeferred: Deferred called back after the last command from the list
                         has been executed or called errback when any of commands 
                         has failed.On success list of C{CommandOutput} are returned
                         and when command fail C{CommandError}.
                         
    @type finalDeferred: C{defer.Deferred}
    
    @ivar output: List of command's output
    @type output: C{list} of C{CommandOutput}
    """
    def __init__(self, commands, deferreds, finalDeferred, user, password, **kwargs):
        if not kwargs.has_key('connection'):
            kwargs['connection']=SSHClientConnection
        SSHClientFactory.__init__(self, finalDeferred, user, **kwargs)
        self.userAuth.password = password

        self.commands = commands
        self.commandsDeferreds = deferreds
        self.finalDeferred = finalDeferred
        self.outputs=[]
        

    def runNextCommand(self):
        """
        Run next command.
        """
        try:
            ch = ExecCmdChannel(self.commands.pop(0), self.commandsDeferreds.pop(0))
            ch.factory = self
        except IndexError:
            self.connection.loseConnection()
            self.finalDeferred.callback(self.outputs)
        else:
            self.connection.openChannel(ch)


    def commandSuccess(self, output, deferred):
        """
        Called by channel when command was executed successfully.
        """
        self.outputs.append(output)
        deferred.callback(output)
        self.runNextCommand()


    def commandFailed(self, output, deferred):
        """
        Called by channel when command has failed.
        """
        deferred.errback(CommandError(output))
        self.connection.loseConnection()
        self.finalDeferred.errback(CommandError(output, self.outputs))


    def errorReceived(self, reason):
        """
        Error occured on lower layer.
        """
        self.finalDeferred.errback(reason)


    def clientConnectionFailed(self, connector, reason):
        """
        Can't connect to a server.
        """
        self.errorReceived(reason)



def SSHRunCommands(commands,
                   user=getenv('LOGNAME'), host='localhost', port=22, password=None, 
                   cmdCallback=None, cmdErrback=None,
                   options=default_config_opts):
                   """
                   Run commands on a host as user using password.
                   Return C{defer.Deferred} which is used to return results.
                   When all commands finish executing it is called back and 
                   if any command fails errback is triggered and execution stops.
                   Callback will return C{list} of C{CommandOutput} and
                   errback C{CommandError}.

                   cmdCallback and cmdErrback arguments may be used to specify
                   functions to execute when a given command execute successfully 
                   or fail respecitvely.Callback receives C{CommandOutput} and errback
                   C{CommandError} as an argument (on errback argument is always wrapped up in 
                   C{python.failure.Failure}).

                   By default user is set to the name of currently logged in user,
                   host to localhost and port to 22.

                   User is authenticated first using SSH Agent then if authentication 
                   fails using password.

                   Different parts of the library can be configured using options.
                   Defaults are stored in default_config_options dictionary.

                   Currently used options:                   
                   Key                      Default value                      Description
                   known_hosts              expanduser('~/.ssh/known_hosts')   Location of the known hosts
                                                                               file

                   known_hosts_autoaddnew  False                               When connecting to
                                                                               unknown host
                                                                               don't verify it's
                                                                               public key, just
                                                                               add it to known hosts file
                                                                               (Useful for testing)

                   auth_methods            ['publickey', 'password']           List of authentication methods
                                                                               to use and order in which
                                                                               they should be tried

                   auth_keys               ['~/.ssh/id_rsa', '~/.ssh/id_dsa']  List of keys to use.Both private
                                                                               key and public key should exist.
                                                                               For example if auth_keys is set to
                                                                               ['~/.ssh/id_rsa'] both private key file 
                                                                               ('id_rsa') and public key file 
                                                                               ('id_rsa.pub') should be accessible.


                   auth_useagent           True                                Use ssh-agent if it is available
                   """
                   commandsDeferreds=[]
                   for cmd in commands:
                       d=defer.Deferred()
                       if cmdCallback:
                           d.addCallback(cmdCallback)
                       if cmdErrback:
                           d.addErrback(cmdErrback)
                       else:
                           pass
                           # If user didn't specify function
                           # to handle command's error ignore it
                           d.addErrback(lambda _: None)
                       commandsDeferreds.append(d)
                   if user is None:
                       raise Error("Can't find name of the currenty logged in user.")
                   finalDeferred=defer.Deferred()
                   factory=SSHExecCmd(commands, commandsDeferreds, finalDeferred, user, password,
                                      config_opts=options)
                   reactor.connectTCP(host, port, factory)
                   return finalDeferred
