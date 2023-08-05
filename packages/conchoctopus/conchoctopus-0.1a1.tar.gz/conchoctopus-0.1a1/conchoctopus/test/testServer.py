#!/usr/bin/env python
"""
I'm simple ssh test server runner.I listen on 100 ports starting from port 6022
and logging every message to standad error.Currently I can execute only a very
limited set of commands (see TestServer class for more details).
"""
from twisted.internet import reactor
from twisted.python import log
from conchoctopus.test.test_connect import TestServer
import sys

log.startLogging(sys.stderr)
start=6022
nlisten=100
ports={}
ts=TestServer()
ts.setUpServer()
for port in range(start, start+nlisten):
    ports[port]=reactor.listenTCP(port, ts.sfactory)
reactor.run()
