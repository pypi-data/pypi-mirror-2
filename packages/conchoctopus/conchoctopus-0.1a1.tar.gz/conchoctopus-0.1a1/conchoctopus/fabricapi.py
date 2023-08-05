#!/usr/bin/env python
from twisted.internet import defer, reactor, utils
from conchoctopus.connect import CommandOutput, CommandError
from conchoctopus.connect import SSHExecCmd, ExecCmdChannel, SSHClientTransport
from conchoctopus.connect import SSHClientConnection, default_config_opts
from twisted.python import log, failure



class FapiTransport(SSHClientTransport):
    def connectionLost(self, reason):
        """
        Notify a task that a connection has been lost.
        """
        if self.factory.task:
            self.factory.task._connectionLost()
        if not self.factory.connectedFired:
            self.factory.connected.callback(None)
        SSHClientTransport.connectionLost(self, reason)



class FapiConnection(SSHClientConnection):
    def serviceStarted(self):
        """
        Notify when client is ready to open channels on a server.
        """
        SSHClientConnection.serviceStarted(self)
        self.factory.connected.callback(None)
        self.factory.connectedFired=True


class FapiExecCmd(SSHExecCmd):
    """
    Client factory that is able to execute commands on demand.

    @ivar connected: C{defer.Deferred} that will be fired
                     when client is ready to do some work or
                     there is a problem with connection
    @type connected: C{defer.Deferred} or C{None} if not set
    
    @ivar connectedFired: set to C{True} when connected deferred
                           was fired or C{False} otherwise
    @type connectedFired: C{Boolean}
    
    @ivar task: a task that use this connection and will be notified
                when the connection is lost
    @type task: C{Task} or C{None} if not set
    """
    connected=None
    connectedFired=False
    task=None


    def runNextCommand(self):
        """
        Don't use the sequential way of running commands.
        """
        return


    def runCommand(self, cmd, cmdDeferred):
        """
        Execute command and use specific deferred
        to handle results and errors.
        """
        ch = ExecCmdChannel(cmd, cmdDeferred)
        ch.factory = self
        self.connection.openChannel(ch)


    def commandFailed(self, output, deferred):
        """
        On error notify only command deferred.
        """
        deferred.errback(CommandError(output))
        self.connection.loseConnection()


    def errorReceived(self, reason):
        """
        Notify connection deferred about an error. 
        """
        self.connected.errback(reason)
        self.connectedFired=True


class Env:
    """
    Each instance of this class store connection 
    dependent data.It shouldn't be modified 
    by users.
    """
    user=None
    host=None
    port=None
    host_string=None
    hosts=None



class Config:
    """
    Class for keeping client configuration data.
    It can be subclassed to create user defined configuration.
    """
    hosts=[]
    password=None
    config_opts=default_config_opts



class FabOutput(str):
    """
    Imitation of fabric output.
    """
    failed=None
    return_code=None
    signal=None



class TaskException(Exception):
    """
    Raised when an exception occurs in task method.
    First argument is always an instance of C{failure.Failure} 
    that represents an exception that terminated a task.The 
    second argument is a result of a clean up method execution.
    It can be either the method's return value or an instance 
    of C{failure.Failure} when an exception has occurred inside
    the method or the method was not implemented.
    """
    def __init__(self, tf, cmr):
        self.taskFailure=tf
        self.cupMethodResults=cmr


    def __str__(self):
        if isinstance(self.taskFailure, Cancelled):
            s='Task stopped.'
        else:
            s='Task failure:\n%s\n' % self.taskFailure.getTraceback()
        if self.cupMethodResults:
            cmr=self.cupMethodResults.getTraceback()
            s+='Clean up method failure:\n%s\n' % cmr
        return s



class Cancelled(Exception):
    """
    Raised by a command when it is cancelled.
    """



def getSignalNames():
    """
    Return a new dictionary where keys are signal codes and 
    values are their symbolic names.
    """
    import signal
    signals={}
    for sym in dir(signal):
        if sym.startswith("SIG"):
            v = getattr(signal, sym)
            if isinstance(v, int):
                signals[v] = sym
    return signals



class _ProcessDeferred:
    """
    A C{defer.Deferred} wrapper that is used with 
    C{utils._EverythingGetter} to intercept its 
    errback's result when a process receives a signal.
    The first argument is an instance of a C{defer.Deferred} 
    that will be used for this purpose.

    This is necessary since C{utils._EverythingGetter} 
    when receiving a signal will errback a tuple which will 
    cause a TypeError exception in C{defer.inlineCallbacks}
    (it calls errback with an argument that is not Exception)
    """
    signalNames=getSignalNames()


    def __init__(self, d):
        self.d=d
        self.callback=lambda r:self.d.callback(r)


    def errback(self, r):
        """
        When receiving a signal this errback is called with a three element 
        tuple as an argument.The last element is a signal's code.A new tuple
        is created from the original one and the signal's name as the last 
        element.The deferred is called back with the tuple as an argument.
        """
        if isinstance(r, tuple):
            self.d.callback(r+(self.signalNames[r[-1]],))
        else:
            self.d.errback(r)



class Commands:
    """
    Implementation of a "built in" commands.
    If connection is not empty it contains tuple
    consisting of client's factory and connection object that 
    is used to close connection.Both cmdDeferreds and cmdResults 
    dictionaries stores data related to a command executed in a job.
    For each job the first contains list of command's C{defer.Deferred} 
    and second its result.Scheduled calls list stores a two item tuples 
    consisting of C{t.i.base.DelayedCall} and the call's deferred.
    Running processes list contains a list of three element tuples
    consisting of C{t.i.i.IProcessTransport} as return by 
    reactor.spawnProcess, command's deferred and a timeToKill value
    that can be specified as an command's argument.Both lists are used 
    when cancelling respective resources.
    
    When cancelling is True resources are being cleaned up and at the
    end of this process the finished cancelling deferred will be fired.
    A disconnect deferred is called back when there is no connection or
    connection is lost.It can also be called by trigger timeout delayed 
    call that is responsible for calling the deferred when specified
    in seconds timeout has passed.
    """


    def __init__(self):
        self._connection=()
        self._cmdDeferreds={}
        self._cmdResults={}
        self._scheduledCalls=[]
        self._runningProcesses=[]

        self.cancelling=False
        self._finishedCancelling=defer.Deferred()
        self._disconnectDeferred=defer.Deferred()
        self._triggerTimeout=None
        self._disconnectTimeout=5


    def _runCmd(self, _, cmd, cmdd):
        """
        Run command on a host.Return specified 
        deferred that will be used to handle
        results.
        """
        c=self._connection[0]
        c.runCommand(cmd, cmdd)
        return cmdd


    def _cbConvertOutput(self, result):
        """
        Return converted result (C{CommandOutput}) to
        fabric compatible output (C{FabOutput}).
        """
        output=FabOutput(result.stdout)
        output.failed=False
        output.return_code=result.exit_code
        return output


    def _cbConvertError(self, f):
        """
        Return converted C{CommandError} to
        fabric compatible output (C{FabOutput}).
        Return failure object if errback was not 
        triggered by C{CommandError}.
        """
        if f.trap(CommandError) == CommandError:
            result=f.value.output
            output=FabOutput(result.stderr)
            output.failed=True
            output.return_code=result.exit_code
            return output
        return f


    def _updateCmdResults(self, r, job):
        """
        Store per job command results.
        """
        self._cmdResults[job].append(r)
        return r


    def run(self, cmd, **kwargs):
        """
        Run command on a server.Return C{defer.Deferred} that will 
        return C{FabOutput} when results become available.
        """
        self._raiseIfCancelled()
        cmdd=defer.Deferred()
        cmdd.addBoth(self._raiseIfCancelled)
        cmdd.addBoth(self._updateCmdResults, self._job_name)
        cmdd.addCallback(self._cbConvertOutput)
        cmdd.addErrback(self._cbConvertError)
        # Connect client if needed.
        if not self._connection:
            f=FapiExecCmd([], [], None, self.env.user, self.config.password, 
                          config_opts=self.config.config_opts, 
                          transport=FapiTransport, connection=FapiConnection)
            f.task=self
            f.connected=defer.Deferred()
            connected=f.connected
            ct=reactor.connectTCP(self.env.host, self.env.port, f)
            self._connection=(f,ct)
        else:
            # Execute command only when client is connected.
            connected=self._connection[0].connected
        connected.addBoth(self._raiseIfCancelled)
        return connected.addCallback(self._runCmd, cmd, cmdd)


    def sleep(self, secs, **kwargs):
        """
        Return C{defer.Deferred} that will
        be fired with an empty string when specified
        number of seconds have passed or with None
        if a task was cancelled before that time.
        """
        self._raiseIfCancelled()
        d=defer.Deferred()
        d.addBoth(self._raiseIfCancelled)
        d.addBoth(self._updateCmdResults, self._job_name)
        self._cmdDeferreds[self._job_name].append(d)
        dc=reactor.callLater(secs, d.callback, '')
        self._scheduledCalls.append((dc, d))
        return d


    def _cbConvertLocalOutput(self, result):
        """
        Convert local output C{tuple} to C{FabOut}.
        """
        if isinstance(result, failure.Failure):
            return result

        out, err, rcode = result[:3]
        if rcode == 0:
            output=FabOutput(out)
            output.failed=False
        else:
            try:
                signame = result[3]
            except IndexError:
                signame = None

            output=FabOutput(err)
            output.failed=True
            output.signal=signame
        output.return_code=rcode
        return output


    def local(self, cmd, timeToKill=5, shellcmd='/bin/sh -c', **kwargs):
        """
        Run command in a local shell.Return C{defer.Deferred}
        that will be called back with C{FabOut} when 
        command exits.

        When cancelling a task the SIGTERM signal will 
        be send to each running process spawned by local.
        If a process is still running after sending the 
        signal a timeToKill argument specify a number of 
        seconds to wait before sending the SIGKILL signal 
        to the process which should abort it unconditionally.
        The default value is five seconds.

        User can specify a shell command that will be used to
        execute the command.
        """
        self._raiseIfCancelled()
        shell=shellcmd.split()[0]
        cmds=tuple(shellcmd.split()[1:])+(cmd,)
        d = defer.Deferred()
        d.addBoth(self._updateCmdResults, self._job_name)
        d.addBoth(self._cbConvertLocalOutput)
        d.addBoth(self._raiseIfCancelled)
        pt=reactor.spawnProcess(utils._EverythingGetter(_ProcessDeferred(d)), shell, 
                                (shell,)+cmds, env={}, path=None)
        self._runningProcesses.append((pt,d,timeToKill))
        self._cmdDeferreds[self._job_name].append(d)
        return d



    def _raiseIfCancelled(self, result=None):
        """
        Raise C{Cancelled} if a cancellation process is in progress 
        or return a result otherwise.This method is invoked directly
        or also as an callback function.
        """
        if self.cancelling:
            self._loseConnection()
            raise Cancelled()
        return result 


    def _cancelTimeout(self, r, dc):
        """
        Cancel delayed call if it's active and return a result.
        """
        if dc.active():
            dc.cancel()
        return r


    def _loseConnection(self):
        """
        If connection is established then try to close it gracefully.
        If it's still open after a timeout number of seconds then 
        force the connection to close.
        """
        if not self._connection:
            return

        if self._connection[1].state == 'connected':
            if not self._triggerTimeout:
                if self._connection[0].connection.transport:
                    self._connection[0].connection.loseConnection()
                    def disconnect():
                        if self._connection[1].state == 'connected':
                            self._connection[1].disconnect()
                        self._disconnectDeferred.callback('Timeout exceeded')
                    self._triggerTimeout=reactor.callLater(
                        self._disconnectTimeout, disconnect)
                else:
                    self._connection[1].disconnect()


    def _connectionLost(self):
        """
        If disconnect timeout is still running then cancel it and notify 
        a cancelling connection deferred.This method is called
        from the connection's transport to notify a task that the
        connection has been lost.
        """
        if self._triggerTimeout:
            if self._triggerTimeout.active():
                self._triggerTimeout.cancel()
        self._disconnectDeferred.callback('Connection lost')



    def cancelResources(self):
        """
        Cancel currently active resources like scheduled function calls,
        running processes and established connections.
        """
        if self.cancelling:
            return
        self.cancelling=True
        cancelDeferreds=[]

        for sc in self._scheduledCalls:
            c, d = sc
            if c.active():
                c.cancel()
                d.callback(None)

        cancelDeferreds.append(self._disconnectDeferred)
        if self._connection:
            self._loseConnection()
        else:
            self._disconnectDeferred.callback('No connection')

        def kill(p, d):
            if p.pid:
                p.signalProcess('KILL')
        for rp in self._runningProcesses:
            p, d, ttk = rp
            p.signalProcess('TERM')
            dc=reactor.callLater(ttk, kill, p, d)
            d.addBoth(self._cancelTimeout, dc)
            cancelDeferreds.append(d)

        cancelDeferreds=defer.DeferredList(cancelDeferreds)
        cancelDeferreds.addBoth(lambda r: 
                                self._finishedCancelling.callback(Cancelled(r)))



class Task(Commands):
    """
    Task that will be executed using given configuration (C{Config})
    and environment (an instance of C{Env}).
    """
    config=None
    env=None

    def __init__(self, config, env):
        self.config=config
        self.env=env
        Commands.__init__(self)


    @defer.inlineCallbacks
    def cleanUpTask(self, exception):
        yield defer.succeed('Clean up method not implemented')



class TaskRunner:
    """
    Task runner is responsible for setting up run time environment 
    where specific methods from a task will be executed using given 
    config.

    @ivar tasks: list of currently configured tasks
    @type tasks: C{list} of C{Task} instances
    """


    def __init__(self):
        self.tasks=[]


    def _runMethod(self, task, method, med, cleanUpMethod='cleanUpTask'):
        """
        Get a method from a task (C{Task}) and run it.Callback method end 
        deferred with a list of task's commands results on success.On error
        run a clean up method and errback the deferred with C{TaskException}.
        """
        def cmResults(cleanUpResult, taskFailure):
            """
            Clean up task and notify method end deferred about errors.
            """
            task.__init__(task.config, task.env)
            med.errback(TaskException(taskFailure, cleanUpResult))
        def runCm(mr):
            """
            Run a clean up method.
            """
            try:
                cm=getattr(task, cleanUpMethod)(mr)
            except Exception, e:
                cmResults(failure.Failure(e), mr)
            else:
                cm.addBoth(cmResults, mr)
        def finishUp(method_result, task, method):
            """
            If an error occurred in a task run a clean up
            method.Otherwise callback a method end deferred
            when all method's deferred finish.
            """
            if isinstance(method_result, failure.Failure):
                if method_result.check(Cancelled) == Cancelled:
                    task._finishedCancelling.addBoth(runCm)
                else:
                    runCm(method_result)
            else:
                defer.DeferredList(task._cmdDeferreds[method]).addBoth(
                    lambda _: med.callback(task._cmdResults[method]))
        task._job_name=method
        getattr(task, method)().addBoth(finishUp, task, method).addErrback(
            log.err)


    def runTask(self, task, methods, config):
        """
        Run methods from C{Task} using C{Config}.
        Methods should be a list of tasks's method names to execute.
        Return list of C{defer.Deferred}s where each one will be used 
        to return results and errors for method running on a host.
        """
        if isinstance(methods, basestring):
            methods=[methods]
        finalDeferreds=[]
        for h in config.hosts:
            user, host = h.split('@')
            port=22
            if host.find(':') != -1:
                host, port = host.split(':')
                port=int(port)
            t=task(config, Env())
            t.env.user=user
            t.env.host=host
            t.env.port=port
            t.env.host_string=h
            self.tasks.append(t)
            def disconnect(_, t):
                if t._connection and t._connection[1].state == 'connected':
                    t._connection[0].connection.loseConnection()
                    t._connection=None
            methodsEndDeferreds=[]
            for method in methods:
                methodEndDeferred=defer.Deferred()
                finalDeferreds.append(methodEndDeferred)
                methodsEndDeferreds.append(methodEndDeferred)
                t._cmdResults[method]=[]
                t._cmdDeferreds[method]=[]
                reactor.callWhenRunning(self._runMethod, t, method, methodEndDeferred)
            defer.DeferredList(methodsEndDeferreds).addCallback(disconnect, t)
        return finalDeferreds



tr=TaskRunner()
_runJobs=tr.runTask
