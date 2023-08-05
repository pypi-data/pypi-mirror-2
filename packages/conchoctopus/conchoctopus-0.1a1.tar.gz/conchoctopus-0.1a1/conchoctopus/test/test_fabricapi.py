from twisted.internet import defer, reactor
from twisted.trial import unittest
from twisted.python import failure
from conchoctopus.connect import CommandOutput, CommandError
from conchoctopus.fabricapi import _runJobs, Task, TaskRunner, TaskException
from conchoctopus.fabricapi import Cancelled
from conchoctopus.test.test_connect import TestChecks, TestServer, changeOpts



class FabricAPIBaseTest(TestChecks, TestServer,unittest.TestCase):
    """
    Base class for tests related to testing Fabric like API.
    """


    def setUp(self):
        """
        Run test server, create client configuration
        and provide fabfile with access to this test case.
        """
        self.setUpServer(port=5022)
        self.Config.config_opts=changeOpts(dict(known_hosts=self.mktemp()))
        self.Task.tc=self


    def setUpTestServers(self):
        """
        For each host defined in test's config run a test server.
        """
        for h in self.Config.hosts:
            ts=TestServer()
            p = h.split(':')[-1]
            ts.setUpServer(port=int(p))
            self.addCleanup(ts.cleanUpServer)
        self.Config.config_opts=changeOpts(dict(known_hosts=self.mktemp()))    



class FabricAPITest(FabricAPIBaseTest):
    """
    Test fabric like API using our test server.
    """
    from conchoctopus.test.fabfile import BasicTask as Task
    from conchoctopus.test.fabfile import BasicConfig as Config

    def test_RunCommandSuccess(self):
        """
        Test executing run command in fabfile.
        """
        fds=_runJobs(self.Task, 'test_success', self.Config)
        def check(r):
            self.assertEqual(r[0][0], True, r)
            self.checkOutput(r[0][1][0], 0, 'run successful cmd', None)
        return defer.DeferredList(fds).addCallback(check)


    def test_RunCommandError(self):
        """
        Test error handling when executing run command in fabfile.
        """
        fds=_runJobs(self.Task, 'test_error', self.Config)
        def check(r):
            self.assertEqual(r[0][0], True, r)
            self.checkOutput(r[0][1][0].value.output, 1, None, 'unknown command')
        return defer.DeferredList(fds).addCallback(check)


    def test_LocalDelays(self):
        """
        See if we can handle delayed asynchronous operations.
        """
        fds=_runJobs(self.Task, 'test_LocalDelays', self.Config)
        def check(r):
            c=r[0][1]
            self.assertEqual(r[0][0], True, r)
            self.assertEqual(c[0], '')
            self.checkOutput(c[1], 0, 'run successful cmd', None)
            self.assertEqual(c[2], '')
            self.checkOutput(c[3], 0, 'run successful cmd', None)
        return defer.DeferredList(fds).addCallback(check)


    def test_FabfileSyntaxError(self):
        """
        Test handling syntax error in fabfile.
        """
        fds=_runJobs(self.Task, 'test_SyntaxError', self.Config)
        def check(r):
            self.assertEqual(r[0][0], False, r)
            self.assertEqual(r[0][1].value.taskFailure.type, NameError)
        return defer.DeferredList(fds, consumeErrors=True).addCallback(check)


    def test_LocalSuccess(self):
        """
        Local command has been executed without any problems.
        """
        fds=_runJobs(self.Task, 'test_LocalSuccess', self.Config)
        def check(r):
            self.assertEqual(r[0][0], True, r[0][1])
            self.assertEqual(r[0][1], [('hello\n', '', 0)], r)
        return defer.DeferredList(fds).addCallback(check)


    def test_LocalError(self):
        """
        Local command has failed.
        """
        fds=_runJobs(self.Task, 'test_LocalError', self.Config)
        def check(r):
            self.assertEqual(r[0][0], True, r)
            self.assertEqual(r[0][1][0][2], 127)
            self.assertEqual(r[0][1][0][1], '/bin/sh: unknown: not found\n')
        return defer.DeferredList(fds, consumeErrors=True).addCallback(check)



class FabricAPITestMultiTask(FabricAPIBaseTest):
    """
    Test running jobs on multiple hosts.
    """
    from conchoctopus.test.fabfile_mtask import MultiTask as Task
    from conchoctopus.test.fabfile_mtask import BasicConfig as Config

    def test_MultiTask(self):
        """
        Run two tasks from fabfile.
        """
        fds=_runJobs(self.Task, ['test_task1', 'test_task2'], self.Config)
        def check(r):
            self.assertEqual(r[0][0], True)
            self.checkOutput(r[0][1][0], 0, 'task1\n', None)
            self.assertEqual(r[1][0], True)
            self.checkOutput(r[1][1][0], 0, 'task2\n', None)
        return defer.DeferredList(fds).addCallback(check)


    def test_MultiTaskDelay(self):
        """
        If one task sleep the other should continue to run.
        """
        fds=_runJobs(self.Task, ['test_task3', 'test_task4'], self.Config)
        def check(r):
            self.assertEqual(self.Task._results, ['task4\n','task3\n'])
            self.assertEqual(r[0][0], True)
            self.checkOutput(r[0][1][0], 0, 'task3\n', None)
            self.assertEqual(r[1][0], True)
            self.checkOutput(r[1][1][0], 0, 'task4\n', None)
        return defer.DeferredList(fds).addCallback(check)



class FabricAPITestMultiHost(FabricAPIBaseTest):
    """
    Enviroment variables gets 
    """
    from conchoctopus.test.fabfile_mhosts import MultiHostTask as Task
    from conchoctopus.test.fabfile_mhosts import MultiHostConfig as Config


    def setUp(self):
        """
        Run test servers and give task's access to the test it will run on.
        """
        self.setUpTestServers()
        self.Task.tc=self


    def test_EnvMix(self):
        """
        Check if environment is consistent before and
        after running a command.
        """
        jobs=['test_task1', 'test_task2']
        fds=_runJobs(self.Task, jobs, self.Config)
        def check(r):
            eb=self.Task.sharedVars.before
            ea=self.Task.sharedVars.after
            nresults=len(self.Config.hosts)*len(jobs)
            self.assertEqual(len(eb), nresults, eb)
            self.assertEqual(len(ea), nresults, ea)
            for host in self.Config.hosts:
                self.assertEqual(eb.count(host), 2, eb)
                self.assertEqual(ea.count(host), 2, ea)
        return defer.DeferredList(fds).addCallback(check)



class FabricAPITestTaskErrorHandling(FabricAPIBaseTest):
    """
    Test handling errors in a task.
    """
    from conchoctopus.test.fabfile import BasicConfig as Config
    class Task(Task):

        @defer.inlineCallbacks
        def runTask(self):
            yield defer.succeed(True)
            raise Exception('task error')



    def setUp(self):
        """
        Create separate task runner for each test.
        """
        FabricAPIBaseTest.setUp(self)
        self.tr=TaskRunner()


    def tearDown(self):
        """
        Delete clean up method if it was defined.
        """
        if getattr(self.Task, 'cleanUpTask', False):
            del self.Task.cleanUpTask


    def check(self, r):
        """
        Test if excepted exception has been raised inside task.
        """
        self.assertEquals(r[0][1].value.taskFailure.value.args, ('task error',))
        return r


    def runCleanUpTest(self, cleanUpMethod, check):
        """
        Run a task and verify its results using a standard check
        and also using the one specified by user.
        """
        if cleanUpMethod:
            self.Task.cleanUpTask=cleanUpMethod.__get__(None, self.Task)
        fds=self.tr.runTask(self.Task, 'runTask', self.Config)
        return defer.DeferredList(fds, consumeErrors=True).addCallback(
            self.check).addCallback(check)


    def test_RunCleanUpMethod(self):
         """
         Test running clean up method.
         """
         @defer.inlineCallbacks
         def cut(self, failure):
             yield defer.succeed(True)
         def check(r):
             self.assertEquals(r[0][1].value.cupMethodResults, None)
         return self.runCleanUpTest(cut, check)


    def test_CleanUpMethodError(self):
        """
        An error occurred when executing a clean up method.
        """
        @defer.inlineCallbacks
        def cut(self, failure):
            raise Exception('clean up error')
        def check(r):
            self.assertEquals(r[0][1].value.cupMethodResults.value.args, ('clean up error',))
        return self.runCleanUpTest(cut, check)



class FabricAPITestCancelResources(FabricAPIBaseTest):
    """
    Test cleaning up different kind of resources.
    """
    timeout=11

    from conchoctopus.test.fabfile import BasicConfig as Config
    class Task(Task):

        @defer.inlineCallbacks
        def csc(self):
            yield self.sleep(10)
            raise Exception("This shouldn't be reached.")

        @defer.inlineCallbacks
        def cc(self):
            yield self.run('echo  ""')
            raise Exception("This shouldn't be reached.")

        @defer.inlineCallbacks
        def cce(self):
            yield self.run('sleep 10')
            raise Exception("This shouldn't be reached.")

        @defer.inlineCallbacks
        def cl(self):
            yield self.local('sleep 10')
            raise Exception("This shouldn't be reached.")

        @defer.inlineCallbacks
        def cdc(self):
            yield self.sleep(0.1)
            yield self.run('echo ""')


    def setUp(self):
        """
        Create a separate task runner for each test.
        """
        FabricAPIBaseTest.setUp(self)
        self.tr=TaskRunner()


    def check(self, r):
        """
        Check if cancelled task and its clean up method returned
        expected results.
        """
        self.assertEquals(type(r[0][1].value), TaskException, r)
        if isinstance(r[0][1].value.taskFailure, failure.Failure):
            r[0][1].value.taskFailure.raiseException()
        self.assertEquals(type(r[0][1].value.taskFailure), Cancelled)
        if isinstance(r[0][1].value.cupMethodResults, failure.Failure):
            r[0][1].value.cupMethodResults.raiseException()
        self.assertEquals(r[0][1].value.cupMethodResults, None)


    def runCancelTest(self, method, cleanUpMethod, delay=None):
        """
        Run a task's method, cancel it and check results.User can specify
        clean up method that will be called just after the cancel.
        """
        self.Task.cleanUpTask=cleanUpMethod.__get__(None, self.Task)
        fds=self.tr.runTask(self.Task, method, self.Config)
        if delay:
            reactor.callLater(delay, self.tr.tasks[0].cancelResources)
        else:
            reactor.callWhenRunning(self.tr.tasks[0].cancelResources)
        return defer.DeferredList(fds, consumeErrors=True).addCallback(self.check)


    def test_CancelScheduledCall(self):
        """
        Test canceling a call scheduled by sleep.
        """
        @defer.inlineCallbacks
        def cleanUpTask(self, r):
            yield defer.succeed(
                self.tc.assertEquals(self._scheduledCalls[0][0].active(), False))
        return self.runCancelTest('csc', cleanUpTask)


    def test_CancelConnectionEstablished(self):
        """
        Test cancelling a connection in 'connected' state.
        """
        @defer.inlineCallbacks
        def cleanUpTask(self, r):
            yield defer.succeed(
                self.tc.assertNotEquals(
                str(self._disconnectDeferred).find('Connection lost'), -1,
                self._disconnectDeferred))

            yield defer.succeed(
                self.tc.assertEquals(
                self._triggerTimeout.active(), False))
        return self.runCancelTest('cce', cleanUpTask, 2)


    def test_CancelLocal(self):
        """
        Test cancelling running processes created by local.
        """
        @defer.inlineCallbacks
        def cleanUpTask(self, r):
            yield defer.succeed(
                self.tc.assertEquals(self._runningProcesses[0][0].pid, None))
            yield defer.succeed(
                self.tc.assertEquals(self._cmdResults['cl'], [('', '', 15, 'SIGTERM')]))
        return self.runCancelTest('cl', cleanUpTask, 2)


    def test_CancelConnectedNoTransport(self):
        """
        Test situation when we're connected but conch's transport
        is not yet available.
        Note: The test is unusual because it's a mix of multi host
        and cancel tests and don't fit any of them perfectly.As more
        bugs will be discovered tests like this one will be common and
        more flexible ways of configuring tests will be needed to avoid
        all those (see below) dirty tricks.
        """
        from conchoctopus.test.fabfile import BasicConfig
        # Make self.check not raise an AttributeError.
        @defer.inlineCallbacks
        def cut(self, r):
            yield defer.succeed(True)
        # By default setUp will run test server on port 5022 and
        # if we use it in a config setUpTestServer will fail because
        # it won't be able to listen on it.
        class Config(BasicConfig):
            hosts=['test@localhost:5023', 'test@localhost:5024']
        # This won't influence any other tests.Trial magic (?)
        self.Config=Config
        self.setUpTestServers()
        return self.runCancelTest('cdc', cut, 0.15)
