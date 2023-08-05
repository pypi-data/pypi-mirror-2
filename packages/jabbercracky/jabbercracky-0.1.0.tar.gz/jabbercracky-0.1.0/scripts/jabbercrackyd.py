#!/usr/bin/env python

LOGFILE = '/var/log/jabbercracky.log'
PIDFILE = '/var/run/jabbercracky.pid'
WORKINGDIR = '/var/run/jabbercracky'

import os, sys
import logging
import jabbercracky
from jabbercracky.jabbercracky import jabbercrackyMain

logging.basicConfig(
                    filename=LOGFILE,
                    filemode='w', # overwrite
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG
                    )

logging.debug('Spawning Daemon...')

if __name__ == "__main__":
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    # decouple from parent environment
    os.chdir("/")   #don't prevent unmounting....
    os.setsid()
    os.umask(0)

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before
            #print "Daemon PID %d" % pid
            open(PIDFILE,'w').write("%d"%pid)
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    # start the daemon main loop
    os.chdir(WORKINGDIR)
    logging.debug('Calling jabbercrackyMain')
    jabbercrackyMain()
