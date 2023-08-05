from twisted.trial import unittest
from twisted.conch.error import ConchError, UserRejectedKey
from twisted.python import log
from conchoctopus.test.test_connect import TestChecks, setUpClient
from conchoctopus.connect import CommandOutput, CommandError, SSHRunCommands, default_config_opts
from os import environ
from sys import stderr
from conchoctopus.test import external_config as default_config
from pprint import pprint

config=default_config
try:
    config=__import__(environ['TEST_CONFIG'])
except KeyError:
    print('\nYou can change default configuration options by setting TEST_CONFIG\n'
          'environment variable to the name of python module that will provide new\n'
          'values.Have a look at default configuration module to see how such module\n'
          'can look like.\n')
except ImportError, e:
    stderr.write("Can't import configuration: %s\n" % e)
except Exception, e:
    stderr.write('Error in configuration: %s\n' % e)
else:
    # Supplement missing options in config module
    # by setting them to default values.
    for sattr in dir(default_config):
        if sattr.startswith('__'):
            continue
        try:
            attr=getattr(config, sattr)
        except AttributeError:
            setattr(config, sattr, getattr(default_config, sattr))
        else:
            # If config options exist in config module
            # supplement them with default options.
            if sattr == 'config_opts':
                co=getattr(default_config, sattr)
                co.update(attr)
                setattr(config, sattr, co)

print('Configuration sources:')
print(default_config)
if config != default_config:
    print(config)
print('\nOptions:')
for o in dir(config):
    if o.startswith('__'):
        continue
    v=getattr(default_config, o)
    if o == 'config_opts':
        print(o+'=')
        for co, cov in v.iteritems():
            print('\t%s=%r' % (co, cov))
    else:
        print('%s=%r' % (o, v))
print('')



class ClientExternalServerTestCase(TestChecks,unittest.TestCase):
    """
    Test client using external server.
    """
    def setUpClient(self, commands):
        """
        Configure client.
        """
        return setUpClient(commands,
                           user=config.user, host=config.host, port=config.port,
                           password=None, config_opts=config.config_opts)


    def printErrors(self, failure):
        """
        Translate some possible errors into more human readable form.
        """
        f=failure.trap(UserRejectedKey, ConchError)
        if f == UserRejectedKey:
            self.fail("%r or its IP can't be found in %r." % (config.host, config.config_opts['known_hosts']))
        elif f == ConchError:
            if failure.value.value == 'NO_MORE_AUTH_METHODS_AVAILABLE':
                self.fail('Authentication failed on %r using user %r.' % (config.host, config.user))
        else:
            return failure


    def test_echo(self):
        """
        Echo string on a server.
        """
        results=self.setUpClient(["echo 'hello'"])
        results.addCallback(lambda r: self.assertEqual(r.pop(0).stdout, 'hello\n'))
        results.addErrback(self.printErrors)
        return results


    def test_unknownCommand(self):
        """
        Run unknown command on a server.
        """
        results=self.setUpClient(["echo 'hello'"])
        results.addErrback(self.printErrors)
        return results
