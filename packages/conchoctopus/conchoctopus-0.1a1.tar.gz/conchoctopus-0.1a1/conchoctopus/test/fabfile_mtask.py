from twisted.internet import defer
from conchoctopus.fabricapi import Task
from conchoctopus.test.fabfile import BasicConfig

class MultiTask(Task):


    @defer.inlineCallbacks
    def test_task1(self):
        x = yield self.run('echo "task1"')


    @defer.inlineCallbacks
    def test_task2(self):
        x = yield self.run('echo "task2"')


    _results=[]
    @defer.inlineCallbacks
    def test_task3(self):
        x = yield self.run('echo "task3"')
        yield self.sleep(1)
        self._results.append(x)


    @defer.inlineCallbacks
    def test_task4(self):
        x = yield self.run('echo "task4"')
        self._results.append(x)
