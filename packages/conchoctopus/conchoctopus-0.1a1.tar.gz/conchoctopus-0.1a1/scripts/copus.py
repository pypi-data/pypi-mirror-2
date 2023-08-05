#!/usr/bin/env python
from conchoctopus import copus
from optparse import OptionParser
from twisted.python import log

parser = OptionParser(
    usage="usage: %prog [options] conchoctopus python module",
    description="Copus is a text user interface for conchoctopus."
                "For more info please visit: "
                "http://bitbucket.org/jakamkon/conchoctopus/wiki/Home")

parser.add_option("-l", "--logfile", dest="logfile", help="Log debug messages to LOGFILE")

(options, pfile) = parser.parse_args()
if len(pfile) < 1:
    parser.error("Please specify a python module where conchocotpus tasks and configs can be found.")

if options.logfile:
    log.startLogging(open(options.logfile, "w+"), setStdout=False)

module=__import__(pfile.pop(0))
copus.run(*copus.getTasksnConfigs(module))
