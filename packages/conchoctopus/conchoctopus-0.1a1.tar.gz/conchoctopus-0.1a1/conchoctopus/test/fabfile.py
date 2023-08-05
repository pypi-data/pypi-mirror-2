from twisted.internet import defer
from conchoctopus.fabricapi import Config, Task


class BasicConfig(Config):
    hosts=['test@localhost:5022']
    password='password'



class BasicTask(Task):


    @defer.inlineCallbacks
    def test_success(self):
        """
        Check if self.environment and command output are correct.
        """
        self.tc.assertEqual(self.env.host_string, 'test@localhost:5022')
        self.tc.assertEqual(self.env.host, 'localhost')
        self.tc.assertEqual(self.env.user, 'test')
        out=yield self.run('run successful cmd')
        self.tc.assertEqual(out, 'run successful cmd')
        self.tc.assertEqual(out.failed, False)
        self.tc.assertEqual(out.return_code, 0)


    @defer.inlineCallbacks
    def test_error(self):
        """
        Check command error output.
        """
        out=yield self.run('run unsuccessful cmd')
        self.tc.assertEqual(out, 'unknown command')
        self.tc.assertEqual(out.failed, True)
        self.tc.assertEqual(out.return_code, 1)


    @defer.inlineCallbacks
    def test_LocalDelays(self):
        yield self.sleep(1)
        yield self.run('run successful cmd')
        yield self.sleep(2)
        yield self.run('run successful cmd')


    @defer.inlineCallbacks
    def test_SyntaxError(self):
        x = yield unknownCmd('')
        y = yield self.sleep(1)


    @defer.inlineCallbacks
    def test_LocalSuccess(self):
        out = yield self.local('echo hello')
        self.tc.assertEqual(out, 'hello\n')
        self.tc.assertEqual(out.failed, False)
        self.tc.assertEqual(out.return_code, 0)


    @defer.inlineCallbacks
    def test_LocalError(self):
        out = yield self.local("unknown")
        self.tc.assertEqual(out.failed, True)
        self.tc.assertEqual(out.return_code, 127)
