from twisted.trial import unittest
from zope.interface import implements
from twisted.conch import avatar, checkers
from twisted.cred import portal
from twisted.protocols import loopback
from twisted.conch.test import keydata
from twisted.python import log
from twisted.python.filepath import FilePath
from twisted.internet import defer, reactor

from twisted.conch.ssh import service
from twisted.conch.ssh import connection, transport, session, factory, userauth, keys
from twisted.conch.error import ConchError, HostKeyChanged, UserRejectedKey

import struct

def setLogPrefix(klass, p='Server: '):
    """
    Change log prefix for a given class.
    """
    class c(klass): pass
    c.__name__  = klass.__name__
    def logPrefix(self):
        return p+klass.logPrefix(self)
    c.logPrefix=logPrefix
    return c

for to_prefix in 'connection.SSHConnection', 'userauth.SSHUserAuthServer', 'session.SSHSession':
    exec(to_prefix+'=setLogPrefix(%s)' % to_prefix)

from conchoctopus.connect import SSHClientTransport, SSHExecCmd, CommandOutput, SSHRunCommands, default_config_opts
from conchoctopus.test.keys import publicKey, privateKey, lockedPublicKey, lockedPrivateKey



class EchoTransport:
    """
    Transport that sends back different exit status and data 
    depending on a command received from a client.
    
    @ivar proto: other end of connection
    @type proto: C{session.SSHSessionProcessProtocol}
    """


    def __init__(self, p):
        self.proto = p
        p.makeConnection(self)
        self.scheduledCalls=[]

    def write(self, data):
        loseConnectionNow=True
        if data == 'run successful cmd':
            self.proto.outReceived(data)
            self.proto.session.conn.sendRequest(self.proto.session, 'exit-status',
                                                struct.pack('>L', 0))
        elif data == 'run unsuccessful cmd':
            self.proto.errReceived("unknown command")
            self.proto.session.conn.sendRequest(self.proto.session, 'exit-status',
                                                struct.pack('>L', 1))
        else:
            cmd=str(data.split()[0])
            if cmd == 'echo':
                arg=str(data.split('"')[1])+'\n'
                self.proto.outReceived(arg)
                self.proto.session.conn.sendRequest(self.proto.session, 'exit-status',
                                                    struct.pack('>L', 0))
            elif cmd == 'sleep':
                arg=str(data.split()[1])
                def wakeUp():
                    self.proto.session.conn.sendRequest(self.proto.session, 'exit-status',
                                                        struct.pack('>L', 0))
                    self.proto.session.loseConnection()
                loseConnectionNow=False
                cl=reactor.callLater(int(arg), wakeUp)
                self.scheduledCalls.append(cl)
            else:
                self.proto.errReceived("unknown command")
                self.proto.session.conn.sendRequest(self.proto.session, 'exit-status',
                                                    struct.pack('>L', 1))
        if loseConnectionNow:
            self.proto.session.loseConnection()


    def loseConnection(self):
        pass


class ConchSessionForTestAvatar:
    """
    Session that delegates executing commands to specific
    transport.

    @ivar avatar: representation of an authenticated user
    @type avatar: C{ConchTestAvatar}

    @ivar proto: client's side of connection
    @type proto: C{session.SSHSessionProcessProtocol}
    """
    implements(session.ISession)


    def __init__(self, avatar):
        self.avatar = avatar
        self.proto = None
        self.transport = None


    def execCommand(self, proto, cmd):
        """
        Connect exec subsystem with transport.
        Send command to the transport.
        
        @param proto: client's side of connection
        @type proto: C{session.SSHSessionProcessProtocol}
        
        @param cmd: command to be executed
        @type: c{str}
        """
        self.proto = proto
        t = EchoTransport(proto)
        self.transport=t
        t.write(cmd)


    def eofReceived(self):
        """
        EOF has been received.
        """
        pass


    def closed(self):
        """
        Notify when session is closed.Cancel unfinished calls.
        """
        if self.transport:
            for sc in self.transport.scheduledCalls:
                if sc.active():
                    sc.cancel()



class ConchTestAvatar(avatar.ConchUser):
    """
    Base class for creating avatars.
    """


    def __init__(self):
        """
        Add C{session.SSHSession} to available channels.
        """
        avatar.ConchUser.__init__(self)
        self.channelLookup.update({'session': session.SSHSession})



class ConchTestRealm:
    """
    I'm generating avatars for an authenticated users.
    """
    implements(portal.IRealm)

    def __init__(self, avatar):
        """
        Store name of user.

        @param avatar: user to be authenticated
        @type avatar: C{avatar.ConchUser}
        """
        self.avatar = avatar


    def requestAvatar(self, avatarID, mind, *interfaces):
        """
        Return a new avatar.If avatar implements a C{logout} method it'll be
        invoked at the end of avatar's existance.
        """
        logout = getattr(self.avatar, 'logout', lambda: None)
        if not callable(logout):
            logout = lambda: None
        return interfaces[0], self.avatar, logout



class ConchTestPasswordChecker:
    """
    Verify user's password.
    """
    credentialInterfaces = checkers.IUsernamePassword,

    def requestAvatarId(self, credentials):
        if credentials.password == 'password':            
            return defer.succeed(credentials.username)
        return defer.fail(ConchError('Wrong password for user %r' % credentials.username))

class ConchTestPublicKeyChecker(checkers.SSHPublicKeyDatabase):
    """
    Verify user's public key.
    """
    def checkKey(self, credentials):
        """
        Allow only known username and key.
        """
        if credentials.username == 'test':
            pkey=keys.Key.fromString(data=publicKey)
            client_pkey=keys.Key.fromString(data=credentials.blob)
            if pkey == client_pkey:
                return True



class ConchTestServerFactory(factory.SSHFactory):
    """
    Glue together various server's components.
    """
    
    userauth.SSHUserAuthServer.attemptsBeforeDisconnect = 2
    services = {
        'ssh-userauth':userauth.SSHUserAuthServer,
        'ssh-connection':connection.SSHConnection
        }
    
    primes = { 2048: [(transport.DH_GENERATOR, transport.DH_PRIME)] }

    publicKeys = { 'ssh-rsa': keys.Key.fromString(keydata.publicRSA_openssh) }
    privateKeys = { 'ssh-rsa': keys.Key.fromString(keydata.privateRSA_openssh) }


    def buildProtocol(self, addr):
        """
        Initialize server's transport and return it.
        """
        proto = transport.SSHServerTransport()
        proto.factory = self
        return proto



class SSHClientTestTransport(SSHClientTransport):
    """
    Test transport that always validates server's key as correct.
    """


    def verifyHostKey(self, hostKey, fingerprint):
        return defer.succeed(0)



from twisted.python import components
components.registerAdapter(ConchSessionForTestAvatar, ConchTestAvatar, session.ISession)

class TestChecks(unittest.TestCase):
    """
    Collection of methods for checking results.
    """


    def checkFailure(self, failure, exception, **kwargs):
        """
        Check if failure was caused by exception and
        if values of exception's attributes match
        those provided by keyword arguments.
        """
        self.assertEqual(failure.trap(exception), exception)
        for earg, value in kwargs.iteritems():
            self.assertEqual(getattr(failure.value, earg), value)


    def checkOutput(self, result, exit_code, stdout, stderr):
        """
        Check if command output contains expected
        value.
        """
        self.assertEqual(result.exit_code, exit_code)
        self.assertEqual(result.stdout, stdout)
        self.assertEqual(result.stderr, stderr)



class TestServer(unittest.TestCase):
    """
    Configure and initialize SSH test server.

    @ivar sfactory: server's factory
    @type sfactory: C{ConchTestServerFactory}

    @ivar server: server's transport
    @type server: C{transport.SSHServerTransport}
    
    @ivar listeningServer: represents server listening on port 
    @type listeningServer: None or an object that provides C{IListeningPort}
    """


    def setUpServer(self, port=None):
        """
        Initialize test server factory and if port is 
        specified start listening on it.
        
        @ivar port: port for server to listen on
        @type port: C{int}
        """
        avatar = ConchTestAvatar()
        realm = ConchTestRealm(avatar)
        p = portal.Portal(realm)
        sshpc = checkers.SSHProtocolChecker()
        sshpc.registerChecker(ConchTestPasswordChecker())
        sshpc.registerChecker(ConchTestPublicKeyChecker())
        p.registerChecker(sshpc)
        self.sfactory = ConchTestServerFactory()
        self.sfactory.portal = p
        self.server = self.sfactory.buildProtocol(None)
        if port:
            self.listeningServer=reactor.listenTCP(port, self.sfactory)
            self.addCleanup(self.cleanUpServer)
        else:
            self.listeningServer=None


    def cleanUpServer(self):
        """
        If there is a listing server disconnect it.
        """
        if self.listeningServer:
            d=self.listeningServer.stopListening()
            def unsetServer(_):
                self.listeningServer=None
            d.addCallback(unsetServer)
            return d
        return defer.succeed()



test_opts=default_config_opts.copy()
test_opts.update(dict(
        known_hosts_autoaddnew=True,
        auth_methods=['password', 'publickey'],
        auth_useagent=False))


def changeOpts(new_opts, defaults=None):
    """
    Return copy of default options with keys and values
    taken from new options.
    """
    if defaults is None:
        defaults=test_opts.copy()
    defaults.update(new_opts)
    return defaults


def setUpClient(commands, 
                user='test', host='localhost', port=5022, password='password',
                config_opts=test_opts):
    """
    Configure client and return C{defer.Deferred}
    for handling results.
    """    
    results=SSHRunCommands(commands, user=user, host=host, port=port, password=password, options=config_opts)
    return results



class ClientFactoryTestCase(TestChecks,TestServer,unittest.TestCase):
    """
    Test client factory using test server factory.

    @ivar cfactory: client's factory
    @type cfactory: C{SSHExecCmd}

    @ivar client: client's transport
    @type client: C{connect.SSHClientTestTransport}/C{SSHClientTestTransport}

    """


    def setUpClientFactory(self, cmds, user='test', password='password', **kwargs):
        """
        Initialze test client factory.

        @param cmd: list of commands to execute
        @type cmd: C{list}
        
        @param user: user used for authentication
        @type user: C{str}
        
        @param password: password used for authentication
        @type password: C{str}
        
        @param kwargs: extra initialization arguments for C{SSHExecCmd}
        @type kwargs: C{dict}
        """
        self.cmdsDeferreds = [defer.Deferred()]
        self.cfactory = SSHExecCmd(cmds, self.cmdsDeferreds, defer.Deferred(), user, password, **kwargs)
        self.client = self.cfactory.buildProtocol(None)
        class MyLoopbackAddress(loopback._LoopbackAddress):
            host = '127.0.0.1'
        # logPrefix method is needed by ssh/service.py to work
        class MyLoopbackTransport(loopback._LoopbackTransport):
            def logPrefix(self):
                return 'loopback'
            def getPeer(self):
                return MyLoopbackAddress()
        loopback._LoopbackTransport = MyLoopbackTransport
        self.cfactory.config_opts['known_hosts']=self.mktemp()
        self.cfactory.config_opts['auth_methods']=['password']
        self.cfactory.config_opts['auth_useagent']=False


    def setUpFactories(self, *args, **kwargs):
        """
        Set up client and server factories.
        """
        self.setUpServer()
        self.setUpClientFactory(*args, **kwargs)


    def test_HostKeyChanged(self):
        """
        Host key does not match the one saved in known_hosts.
        """
        localhost_hash="|1|3WSoctghs4MSv+37IZq+WHJdppc=|OECqGXrA9ZV2QGwGpNzfdaOd0T0="         
        localhost_addr_hash="|1|ek4Sqr6THA7deSSGv+CJO+FEyXs=|Qh7kT0U+S9i\yJZkicB77BoxsiU8="
        ktype, pkey, _ =keydata.publicRSA_openssh.split()
        badpkey=ktype+' '+pkey[:-1]+pkey[-1].lower()
        kh=''.join(localhost_hash+' '+badpkey+' '+localhost_addr_hash+badpkey)
        self.setUpFactories([''])
        FilePath(self.cfactory.config_opts['known_hosts']).setContent(kh)
        self.cfactory.finalDeferred.addErrback(self.checkFailure, HostKeyChanged)
        loopback.loopbackAsync(self.server, self.client)
        return self.cfactory.finalDeferred


    def test_HostKeyDisableAutoAddNew(self):
        """
        Reject a new host key if user wants it.
        """
        self.setUpFactories([''])
        FilePath(self.cfactory.config_opts['known_hosts']).setContent('')
        self.cfactory.config_opts['known_hosts_autoaddnew']=False
        self.cfactory.finalDeferred.addErrback(self.checkFailure, UserRejectedKey)
        loopback.loopbackAsync(self.server, self.client)
        return self.cfactory.finalDeferred


    def test_FailedAuth(self):
        """
        Test handling authentication failure.
        """
        self.setUpFactories([''], 'user', 'wrong password', transport=SSHClientTestTransport)
        loopback.loopbackAsync(self.server, self.client)
        self.cfactory.finalDeferred.addErrback(self.checkFailure,
                                               ConchError,
                                               value='NO_MORE_AUTH_METHODS_AVAILABLE',
                                               data='no more authentication methods available')
        return self.cfactory.finalDeferred


    def test_ExecCmd(self):
        """
        Test successful command execution.
        """
        from twisted.internet.base import DelayedCall
        DelayedCall.debug = True
        self.setUpFactories(['run successful cmd'], transport=SSHClientTestTransport)
        self.cmdsDeferreds[0].addCallback(
            lambda r: self.checkOutput(r, 0, 'run successful cmd', None))
        self.cfactory.finalDeferred.addCallback(
            lambda r: self.checkOutput(r[0], 0, 'run successful cmd', None))       
        loopback.loopbackAsync(self.server, self.client)
        return self.cfactory.finalDeferred


    def test_ExecCmdFailed(self):
        """
        Test failed command execution.
        """
        self.setUpFactories(['run unsuccessful cmd'], transport=SSHClientTestTransport)
        self.cmdsDeferreds[0].addErrback(
            lambda f: self.checkOutput(f.value.output, 1, None, 'unknown command'))
        self.cfactory.finalDeferred.addErrback(
            lambda f: self.checkOutput(f.value.output, 1, None, 'unknown command'))
        loopback.loopbackAsync(self.server, self.client)
        return self.cfactory.finalDeferred



class ClientServerTestCase(TestChecks,TestServer,unittest.TestCase):
    """
    Test client using test server via TCP connection.
    """


    def setUpClientServer(self, commands, **kwargs):
        """
        Run commands on test server.
        """
        self.setUpServer(port=5022)
        self.opts=changeOpts(dict(known_hosts=self.mktemp()))
        self.opts.update(kwargs)
        return setUpClient(commands, port=5022, config_opts=self.opts)


    def test_RunCommandSuccess(self):
        """ 
        Run successful command and get results.
        """
        results=self.setUpClientServer(['run successful cmd'])
        results.addCallback(
            lambda r: self.checkOutput(r[0], 0, 'run successful cmd', None))
        return results 


    def test_RunCommandFailed(self):
        """
        Run failed command and get results.
        """
        results=self.setUpClientServer(['run unsuccessful cmd'])
        results.addCallback(
            lambda r: self.fail('Callback was called intead of errback.'
                                'Callback results: %r' % r))
        results.addErrback(
            lambda f: self.checkOutput(
                    f.value.output, 1, None, 'unknown command'))
        return results 


    def setUpClientPKAuth(self, commands, publicKey, privateKey):
        """
        Create keys and configure client to use them.
        """
        kpath=self.mktemp()
        FilePath(kpath).setContent(privateKey)
        FilePath(kpath+'.pub').setContent(publicKey)
        return self.setUpClientServer(commands, password=None,
                                    auth_methods=['publickey'],
                                    auth_keys=[kpath])


    def test_PKAuth(self):
        """
        Authenticate client using public key.
        """
        return self.setUpClientPKAuth(
            ['run successful cmd'], 
            publicKey, 
            privateKey).addCallback(
                lambda r: self.checkOutput(r[0], 0, 'run successful cmd', None))


    def test_EncryptedKeyAuth(self):
        """
        Try to use encrypted key which is not supported.
        """
        return self.setUpClientPKAuth(
            [''],
            lockedPublicKey, 
            lockedPrivateKey).addCallback(
                lambda r: self.fail('Callback was called intead of errback.'
                                    'Callback results: %r' % r)).addErrback(
                                        self.checkFailure,
                                        ConchError,
                                        value='NO_MORE_AUTH_METHODS_AVAILABLE',
                                        data='no more authentication methods available')
