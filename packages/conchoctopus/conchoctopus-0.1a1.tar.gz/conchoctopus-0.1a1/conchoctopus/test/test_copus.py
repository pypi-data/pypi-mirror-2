from twisted.trial import unittest
from twisted.internet import reactor, defer
from twisted.python.filepath import FilePath

from conchoctopus.test.test_fabricapi import FabricAPIBaseTest
from conchoctopus.copus import TextUI, defaultPalette
from conchoctopus.fabricapi import Task, Config
from conchoctopus.test import keys
from conchoctopus.test.test_connect import test_opts

import urwid
import urwid.raw_display
from urwid.main_loop import TwistedEventLoop

import StringIO
import sys



class FakeStdout(StringIO.StringIO):
    """
    A stdout like object that stores internally everything that it receives.
    """
    def fileno(self):
        return sys.stdout.fileno() 



class FakeStdin(StringIO.StringIO):
    """
    A stdin like object that stores internally everything that it receives.
    """
    def fileno(self):
        return sys.stdin.fileno()



class TestScreen(urwid.raw_display.Screen):
    """
    A screen that captures both stdin and stdout.
    """
    def __init__(self, *args, **kwargs):
        urwid.raw_display.Screen.__init__(self, *args, **kwargs)
        self._term_output_file = FakeStdout()
        self._term_input_file = FakeStdin()



def genhosts(n, userhost='test@localhost:', firstport=4022):
    """
    Return a C{list} of n host strings and connect each with a consecutive port
    starting from firstport.
    """
    return [userhost+str(port) for port in range(firstport, firstport+n)]



class UCopusBaseTest(FabricAPIBaseTest):
    """
    Base test for testing text user interface.
    """
    def setUp(self):
        """
        Configure user interface for testing environment.
        """
        self.ui=TextUI([self.Task], [self.Config])
        self.screen=TestScreen()
        self.loop = urwid.MainLoop(self.ui.main, defaultPalette, screen=self.screen, 
                              event_loop=TwistedEventLoop(reactor),
                              unhandled_input=self.ui.handleControls)
        self.ui.screen=self.screen
        self.ui.mloop=self.loop
        self.screen.start()
        def clean():
            if self.ui.updateScreenCall:
                self.ui.updateScreenCall.stop()
        self.addCleanup(clean)


    def tearDown(self):
        """
        Stop the screen.
        """
        self.screen.stop()


    def setUpTestServers(self):
        """
        Run test servers, create a test public/private key pair and create test
        options.
        """
        FabricAPIBaseTest.setUpTestServers(self)
        kp=self.mktemp()
        FilePath(kp).setContent(keys.privateKey)
        FilePath(kp+'.pub').setContent(keys.publicKey)
        self.Config.config_opts=test_opts.copy()
        self.Config.config_opts.update(dict(known_hosts_autoaddnew=True,
                                            known_hosts=self.mktemp(),
                                            auth_keys=[kp]))



class UCopusSimpleTest(UCopusBaseTest):
    """
    Test simple module.
    """
    timeout=5
    class Task(Task):
        @defer.inlineCallbacks
        def runTask(self):
            x=yield self.run('echo "hello"')
            if x.failed:
                raise Exception('Command failed')

    class Config(Config):
        hosts=['test@localhost:5022']


    def test_ConnectionRefused(self):
        """
        Check when server is not responding.
        """
        def check(r):
            self.assertEqual(self.ui.status.get_text()[0], 'Finished.')
            for i, h in enumerate(self.Config.hosts):
                self.assertEqual(self.ui.tasksStatus[h].get_text()[0], '-')
                self.assertNotEqual(
                    self.ui.errorsContent[i].get_text()[0].find('Connection refused'), -1)
        self.ui.handleControls('r')
        return defer.DeferredList(self.ui.fds).addBoth(check)

    
    def checkFinishedRun(self, r):
        """
        Check gobal status and status of each task when 'run' command has been
        finished.
        """
        self.assertEqual(self.ui.status.get_text()[0], 'Finished.')
        for h in self.Config.hosts:
            msgs=self.ui.tasksStatus[h]
            self.assertEqual(msgs.get_text()[0], 'v', repr(msgs.get_text()[0]))
        return r


    def test_Run(self):
        """
        Test running task.
        """
        self.setUpTestServers()
        self.ui.handleControls('r')
        reactor.callWhenRunning(self.assertEqual, self.ui.status.get_text()[0], 'Running...')
        return defer.DeferredList(self.ui.fds).addBoth(self.checkFinishedRun)


    def test_Rerun(self):
        """
        Test running command after one 'run' command has been executed.
        It checks if UI environment is cleaned up after each run.
        """
        d=defer.Deferred()
        def first(r):
            self.ui.handleControls('r')
            for i, h in enumerate(self.Config.hosts):
                msgs=self.ui.tasksStatus[h]
                self.assertEqual(msgs.get_text()[0], '')
                self.assertEqual(self.ui.errorsContent, [])
            defer.DeferredList(self.ui.fds).addBoth(self.checkFinishedRun).addBoth(d.callback)
        self.test_Run().addBoth(first)
        return d


    def test_Stop(self):
        """
        Test stopping task.
        """
        self.setUpTestServers()
        self.ui.handleControls('r')
        reactor.callWhenRunning(self.ui.handleControls, 's')
        reactor.callWhenRunning(self.ui.handleControls, 'y')
        def check(r):
            for i, h in enumerate(self.Config.hosts):
                msgs=self.ui.tasksStatus[h]
                self.assertEqual(msgs.get_text()[0], '-')
                self.assertEqual(self.ui.errorsContent[i].get_text()[0], '%d %s:\n'
                                                        'Task stopped.' % (i+1, h))
                self.assertEqual(self.ui.status.get_text()[0], 'Stopped.')
        return defer.DeferredList(self.ui.fds).addBoth(check)



class UCopusSimpleTestATenHosts(UCopusSimpleTest):
    """
    Perform basic tests on ten hosts.
    """
    class Config(Config):
        hosts=genhosts(10)



class UCopusSimpleTestBFiftyHosts(UCopusSimpleTest):
     """
     Perform basic tests on fifty hosts.
     """
     timeout=50
     class Config(Config):
         hosts=genhosts(50)



class UCopusSimpleTestCOneHundredHosts(UCopusSimpleTest):
     """
     Perform basic tests on one hundred hosts.
     """
     timeout=100
     class Config(Config):
         hosts=genhosts(100)

