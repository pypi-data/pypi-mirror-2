"""
This is Conchoctopus test module that is meant to be run by copus.py utility.
Before it can be used test server should be running.You can do that by simply
running conchocotpus.test.testServer module.
"""
from twisted.internet import defer
from twisted.python import log
from conchoctopus.fabricapi import Config, Task
from conchoctopus.connect import default_config_opts
from conchoctopus.test import keys
import random
from datetime import datetime
from twisted.python.filepath import FilePath



class TestConfig(Config):
    """
    A simple test config that defines one hundred test hosts to connect.
    It will create its own known_hosts file and propagate it as needed.
    New public keys are accepted by default from each server that we try
    to connect to.
    """
    nhosts=100
    hosts=['test@localhost:'+str(port) for port in range(6022, 6022+nhosts)]
    config_opts=default_config_opts
    k='/tmp/copustestModuleKey'
    FilePath(k).setContent(keys.privateKey)
    FilePath(k+'.pub').setContent(keys.publicKey)
    config_opts.update(dict(known_hosts_autoaddnew=True,
                            known_hosts='/tmp/known_hosts',
                            auth_keys=[k]))

class TestTask(Task):
    """
    Task that shows an asynchronous nature of Conchocotpus.Each running
    task on a particular host will be delayed using a random time and
    during that time the other tasks can still be running.Every task
    that runs on a server that listens on port that ends with number
    one will raise an exception.
    """
    f=open('/tmp/copus_testModule.log', 'w+')

    @defer.inlineCallbacks
    def runTask(self):
        """
        This method is required and it's an entry point for each task.       
        """
        r=yield self.run('echo "hello"')
        if r.failed:
            raise Exception('Remote echo command failed on %s' % self.env.host_string)
        yield self.sleep(random.randrange(10, 20))
        if self.env.host_string.endswith('1'):
            raise Exception('Test exception from %s' % self.env.host_string)
        yield defer.succeed(self.f.write("%s\t%s\n" % (datetime.now(), self.env.host_string)))
        yield defer.succeed(self.f.flush())

    @defer.inlineCallbacks
    def cleanUpTask(self, error):
        """
        This method is not required, but it will be invoked
        when an exception was raised inside runTask.
        """
        yield defer.succeed(True)
