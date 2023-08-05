from twisted.internet import defer
from conchoctopus.fabricapi import Task
from conchoctopus.test.fabfile import BasicConfig



class MultiHostConfig(BasicConfig):
    """
    Generate nhosts host entries.
    """
    nhosts=2
    hosts=['test@localhost:'+str(port) for port in range(5022, 5022+nhosts)]



class MultiHostTask(Task):
    class sharedVars:
        before=[]
        after=[]



    @defer.inlineCallbacks
    def test_task1(self):
        self.sharedVars.before.append(self.env.host_string)
        yield self.run('echo "task1"')
        self.sharedVars.after.append(self.env.host_string)


    @defer.inlineCallbacks
    def test_task2(self):
        self.sharedVars.before.append(self.env.host_string)
        yield self.run('echo "task2"')
        self.sharedVars.after.append(self.env.host_string)

