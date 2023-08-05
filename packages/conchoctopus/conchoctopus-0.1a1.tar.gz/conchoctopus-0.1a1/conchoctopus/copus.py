#!/usr/bin/env python
import urwid
import urwid.raw_display
from urwid.main_loop import TwistedEventLoop

from twisted.internet import reactor, defer
from twisted.internet.task import LoopingCall
from twisted.python import log, failure

from conchoctopus.fabricapi import TaskRunner, Config, Task

import types
from datetime import datetime



class TextUI:
    """
    Text user interface class.
    
    @ivar tasks: C{list} of C{Task}s

    @ivar configs: C{list} of C{Config}s
    
    We're currently using only the first element from each list.
    
    @ivar mloop: C{urwid.MainLoop} object that runs the UI

    @ivar screen: C{urwid.raw_display.Screen} object that we draw UI on

    @ivar currentTask: C{fabricapi.Task} that we're currently using

    @ivar currentConfig: C{fabricapi.Config} that we're currently using

    @ivar taskRunner: C{fabricapi.TaskRunner} that runs current task using
                      current config

    @ivar fds: C{list} of tasks' C{defer.Deferred}s as returned by
               C{fabricapi.TaskRunner.runTask}

    @ivar updateScreenCall: C{task.LoopingCall} that periodically update
                            the screen

    @ivar errorView: C{True} when error logs are currently displayed

    @ivar isRunning: C{True} when tasks are running

    @ivar stopped: C{True} when tasks has been stopped by a user

    @ivar requests: C{list} used to track keys (commands) confirmations

    @ivar oldStatus: C{str} that holds command's status just before a
                     confirmation, it is used when user say 'no' to
                     the confirmation

    @ivar executedTasks: a number of tasks that has been executed

    @ivar failedTasks: a number of tasks that has failed (including
                       those that haven't been yet executed)

    @ivar succeededTasks: a number of tasks that has succeeded

    @ivar tasksNum: a total number of configured tasks ready to be executed

    @ivar hostsNum: C{list} of hosts IDs (numbers from 1 to the number of hosts)


    Widgets:
    @ivar tasksStatus: C{dict} where each key is a host string and every value is
                       C{urwid.Text} that is either 'v' on success, '-' on failure
                       or empty string when status is not yet known

    @ivar h1: C{urwid.Text} that contains top header's content

    @ivar hdr1: h1 colored using C{urwid.attrWrap}

    @ivar fields: C{urwid.Colums} with column's names
    
    @ivar header: C{urwid.Pile} that contains both hdr1 and fields and is
                  located in the first two rows of the screen

    @ivar body: C{urwid.ListBox} that represents list of all hosts to run
                and their current status for current task

    @ivar errorHeader: C{urwid.Pile} that contains hdr1 and a 'Current
                       error logs' text
    
    @ivar errors: C{urwid.ListBox} that represents a list of all errors for
                  all hosts for current task (it uses errorsContent list
                  as a source of data)

    @ivar status: C{urwid.Text} that contains current status of tasks' execution
                  or questions that requires confirmation from a user

    @ivar pstatus: c{urwid.Text} set to a percentage of tasks that has been executed,
                   those that has succeeded and those that has failed

    @ivar footer: C{urwid.Columns} that contains both status and pstatus

    @ivar main: C{urwid.Frame} that glue together header, body and footer and
                when error logs are displayed some of them are replaced by their
                error related equivalents such as errorHeader and errors
    """
    def __init__(self, tasks, configs):
        self.mloop=None
        self.screen=None
        
        self.currentTask=tasks[0]
        self.currentConfig=configs[0]
        self.taskRunner=None
        self.fds=None

        self.updateScreenCall=None
        self.errorView=False
        self.isRunning=False
        self.stopped=False
        self.requests=[]
        self.oldStatus=None

        self.executedTasks=0
        self.failedTasks=0
        self.succeededTasks=0

        self.tasksNum=len(self.currentConfig.hosts)*len(tasks)

        self.h1 = urwid.Text('Config: %s - %d hosts %s tasks' % (
                self.currentConfig, len(self.currentConfig.hosts), len(tasks)))

        controls=[]
        controls.append('[')
        for c in ('run','stop','quit','errors'):
            controls.extend([('keys',c[0]), c[1:]+'|'])
        self.hdr1 = urwid.Columns([
            urwid.AttrWrap(self.h1, 'head'),
            ('fixed', 40,
             urwid.AttrWrap(urwid.Text(controls+['Up/Down/PgUp/PgDn]']), 'head'))])
        self.fields = urwid.Columns([ ('fixed', 5, urwid.Text('ID')), 
                                      urwid.Text('username@hostname[:port]'), urwid.Text(str(tasks[0])) ])
        self.header = urwid.Pile([self.hdr1, self.fields])

        self.hostsNum=range(1, len(self.currentConfig.hosts)+1)
        self.tasksStatus={}.fromkeys(self.currentConfig.hosts)

        bodyContent=[]
        for i, h in zip(self.hostsNum, self.currentConfig.hosts):
            status=urwid.Text('')
            self.tasksStatus[h]=status
            bodyContent.append(urwid.Columns(
                [('fixed', 5, urwid.Text(str(i))),
                 urwid.Text(h),
                 status]))

        self.body = urwid.ListBox(bodyContent)
        
        self.errorHeader = urwid.Pile([self.hdr1, urwid.Text('Current error logs:')])
        self.errorsContent=[]
        self.errors = urwid.ListBox(self.errorsContent)

        self.status=urwid.Text('Not running.')
        self.pstatus=urwid.Text('', align='right')
        self.footer=urwid.Columns([('fixed', 15, self.status), self.pstatus])
        self.main=urwid.Frame(urwid.AttrWrap(self.body, 'body'),
                                header=self.header, 
                                footer=urwid.AttrWrap(self.footer, 'foot'))
        reactor.callWhenRunning(self.updateScreen, start=True)


    def updateScreen(self, start=False):
        """
        Update screen with a fresh data.If start is True start running the
        update every one second.
        """
        if start:
            self.updateScreenCall=LoopingCall(self.updateScreen)
            self.updateScreenCall.start(1, now=True)
            return
        self.pstatus.set_text(self.getpStatus())
        self.mloop.draw_screen()


    def storeTaskStatus(self, result, i, host, task):
        """
        Triggered when task has finished.Increment tasks' counters and set both
        global status and tasks' status accordingly.
        """
        self.executedTasks+=1
        if self.executedTasks == self.tasksNum:
            if self.stopped:
                self.status.set_text('Stopped.')
            else:
                self.status.set_text('Finished.')
            self.isRunning=False
        if isinstance(result, failure.Failure):
            self.tasksStatus[host].set_text('-')
            e=urwid.Text('%d %s:\n%s' % (i, host, result.value))
            self.errorsContent.append(e)
            self.errorsContent.sort(
                key=lambda x: int(x.get_text()[0][:10].split()[0]))
            self.failedTasks+=1
        else:
            self.tasksStatus[host].set_text('v')
            self.succeededTasks+=1
        return None


    def runTask(self):
        """
        Run current task.Reset tasks' counters and each tasks' status.
        Using C{fabcricapi.TaskRunner} run each task and for each returned
        C{defer.Deferred} add both callback and errback to handle future
        results.
        """
        self.isRunning=True
        self.status.set_text('Running...')
        self.executedTasks=0
        self.failedTasks=0
        self.succeededTasks=0
        for h in self.currentConfig.hosts:
            self.tasksStatus[h].set_text('')
            self.errorsContent=[]
            self.errors = urwid.ListBox(self.errorsContent)
            
        self.taskRunner=TaskRunner()
        self.fds=self.taskRunner.runTask(self.currentTask, 'runTask',
                                    self.currentConfig)
        for i, host in zip(self.hostsNum, self.currentConfig.hosts):
            self.fds[i-1].addBoth(self.storeTaskStatus, i, host, self.currentTask)


    def getpStatus(self):
        """
        Return triple of percentage of tasks finished, finished successfully
        and failed.
        """
        pe=(float(self.executedTasks)/float(self.tasksNum))*100
        ps=(float(self.succeededTasks)/float(self.tasksNum))*100
        pf=(float(self.failedTasks)/float(self.tasksNum))*100
        return '%d%% tasks executed (%d%% succeeded/%d%% failed)' % (pe, ps, pf)


    def quit(self, answer):
        """
        If a user has confirmed quitting then stop reactor otherwise set status
        to the one that was before confirmation.
        """
        if answer == 'y':
            reactor.stop()
        else:
            self.status.set_text(self.oldStatus)


    def stop(self, answer):
        """
        If a user has confirmed stopping tasks then cancel each task otherwise
        set status to the one that was before confirmation.
        """
        if answer == 'y':
            self.status.set_text('Stopping...')
            cancelled=[]
            for rt in self.taskRunner.tasks:
                rt.cancelResources()
                cancelled.append(rt._finishedCancelling)
                defer.DeferredList(cancelled).addCallback(
                    lambda _: setattr(self, 'stopped', True))
        else:
            self.status.set_text(self.oldStatus)


    def handleControls(self, key):
        """
        Handle control keys.
        """
        if key in ('y', 'Y', 'n', 'N'):
            if self.requests:
                r=self.requests.pop(0)
                getattr(self, r)(key.lower())
        elif key in ('q', 'Q'):
            if 'quit' not in self.requests:
                self.requests.append('quit')
                self.oldStatus=self.status.get_text()[0]
                self.status.set_text('Quit? [y/n]')
        elif key in ('r', 'R'):
            if not self.isRunning:
                self.runTask()
        elif key in ('s', 'S'):
            if self.isRunning:
                if 'stop' not in self.requests:
                    self.requests.append('stop')
                    self.oldStatus=self.status.get_text()[0]
                    self.status.set_text("Really stop? [y/n]")
        elif key in ('e', 'E'):
            if self.errorView:
                self.main.set_header(self.header)
                self.main.set_body(self.body)
                self.errorView=False
            else:
                self.main.set_header(self.errorHeader)
                self.main.set_body(self.errors)
                self.errorView=True


defaultPalette = [
    ('head', 'white', 'black'),
    ('keys', 'white,underline', 'black'),
    ('body', 'default', 'default'),
    ('foot', 'light gray', 'black')
    ]


def run(tasks, configs):
    """
    Configure necessary components to run tasks using configs in text user
    interface.
    """
    ui=TextUI(tasks, configs)
    screen=urwid.raw_display.Screen()
    loop = urwid.MainLoop(ui.main, defaultPalette, screen=screen, 
                      event_loop=TwistedEventLoop(reactor),
                      unhandled_input=ui.handleControls)
    ui.screen=screen
    ui.mloop=loop
    loop.run()


def getTasksnConfigs(module):
    """
    Return a tuple of tasks and configs taken from module.
    Skip names that begin with double underscore.
    """
    tasks=[]
    configs=[]
    for cls in dir(module):
        if cls.startswith('__'):
            continue
        c=getattr(module, cls)
        if type(c) is types.ModuleType:
            continue
        try:
            if issubclass(c, Task) and c is not Task:
                tasks.append(c)
            elif issubclass(c, Config) and c is not Config:
                configs.append(c)
        except TypeError, e:
            continue
    return (tasks, configs)
