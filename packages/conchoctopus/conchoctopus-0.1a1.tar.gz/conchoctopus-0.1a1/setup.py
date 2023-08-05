#!/usr/bin/env python
from distutils.core import setup
from conchoctopus import __version__

setup(name='conchoctopus',
      version=__version__,
      description="An environment and API that simplifies working"
                  "with multiple SSH servers in an asynchronous way.",
      long_description="""\
Provides an asynchronous execution environment and Python class and
inlineCallbacks based API for exchanging data between local and
remote systems.""",
      author='Kuba Konczyk',
      author_email='jakamkon@gmail.com',
      url='http://bitbucket.org/jakamkon/conchoctopus/',
      license='MIT',
      packages=['conchoctopus', 'conchoctopus.test'],
      scripts=['scripts/copus.py'],
      requires=['Python (>=2.5)', 'Twisted (>=8.2)', 'Urwid (>=0.9.9)'],
      test_suite='conchoctopus.test',
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Framework :: Twisted',
                   'Intended Audience :: Developers',
                   'Intended Audience :: System Administrators',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.5',
                   'Topic :: System :: Clustering',
                   'Topic :: System :: Distributed Computing',
                   'Topic :: System :: Systems Administration'])
