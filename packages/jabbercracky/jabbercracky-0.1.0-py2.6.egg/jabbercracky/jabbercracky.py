#
#  JabberCracky main method
#  - Start Pool of Workers
#
#  NOTE: charset.txt must be in the CWD or rcracki_mt fails

import MySQLdb, os
from multiprocessing import Pool
import time
import ConfigParser

# debugging aids
import sys
import traceback

import logging
import pipes

# the possible values of the 'state' SQL column
state_NEW       = 0;  # Starts here, run by phase 1
state_RUNNING   = 20; # Used by both phases when running
state_P1WON     = 30; # Solved by phase 1
state_P1LOST    = 40; # Not solved by phase 1
state_P2WON     = 50; # Solved by phase 2
state_P2LOST    = 60; # Not solved by phase 2

def formatExceptionInfo(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)

def connectDB():
    global config,conn
    if conn:
        try:
            conn.ping()
        except MySQLdb.OperationalError:
            conn = None
    if not conn:
        logging.debug( 'Connecting to MySQL' )
        conn = MySQLdb.connect(host = config.get('db', 'host'),
                               user = config.get('db', 'user'),
                               passwd = config.get('db', 'passwd'),
                               db = config.get('db', 'database'))

def crackWorker(id, hash, type):
    global config,conn
    filename = str(id)+'.txt'
    s = config.get('fs', 'rcracki')+' -h '+hash+' -o '+filename+' -t ' \
        + config.get('tune', 'threads_per_proc')+' ' \
        + config.get('fs', 'rainbow_tables')+'/'+type

    logging.debug( 'crackWorker CWD is '+ os.getcwd() )
    logging.debug( 'crackWorker CMD is '+s )
    fd = os.popen(s)
    fd.read() # we don't want the output, just need to block
    fd.close()

    # if the hash is there, add it to the db
    try:
        f = open(filename, 'r')
        for line in f.readlines():
            # hash:clear:???
            words = line.split(':')
            setClearStateByHash(words[0],words[1],state_P1WON)
        f.close()
        # maybe delete file here?
        
    # otherwise, set this to failed state
    except:
        logging.debug( formatExceptionInfo() )
        setStateById(id, state_P1LOST)

def setRunningById(id):
        global config,conn
        bq = """
        UPDATE queue SET state=20,started=now(),maxcpu={0!s},threads={1!s} WHERE id={2!s}
        """
        maxProcs = int(config.get('tune', 'max_procs'))    
        
        connectDB()
        c = conn.cursor()
        c.execute("SET AUTOCOMMIT=1")
        c.execute(bq.format(maxProcs, config.get('tune', 'threads_per_proc'), id))
        c.close()

def setStateById(id, state, lastpw = ''):
        global config,conn
        bq = """
        UPDATE queue SET state={0!s},lastpw='{2!s}' WHERE id={1!s}
        """
        connectDB()
        c = conn.cursor()
        c.execute("SET AUTOCOMMIT=1")
        logging.debug('lastpw in setstate: '+lastpw)
        c.execute(bq.format(state,id,lastpw))
        c.close()

def setClearStateByHash(hash,clear,state):
        global config,conn
        aq = """
        UPDATE queue SET state={0!s},clear='{1!s}',cracked=now() WHERE hash='{2!s}'
        """
        connectDB()
        c = conn.cursor()
        c.execute("SET AUTOCOMMIT=1")
        c.execute(aq.format(state,clear,hash))
        c.close()

def getByState(state):
        global config,conn
        bq = """
        SELECT * FROM queue WHERE state={0!s}
        """
        connectDB()
        c = conn.cursor()
        c.execute("SET AUTOCOMMIT=1")
        c.execute(bq.format(state))
        rows = c.fetchall()
        c.close()
        return rows

def gpuWorker(id, hash, start_pw=''):
    global config,conn    
    try:
        s = config.get('fs', 'gpucrack')+' -c 7 -h '+hash

        if len(start_pw) >0:
            s = s+' -s '+pipes.quote(start_pw)
    
        logging.debug( 'gpuWorker CWD is '+ os.getcwd() )
        logging.debug( 'gpuWorker CMD is '+s )
        fdin, fdouterr = os.popen4(s)
        output = fdouterr.read()
        
        #logging.debug(output)
        
        errStr = "Init Bruteforce error"
        loseStr = "no password found"
        lastPwStr = "End Pwd:"
        winStr = "MD5 Cracked pwd="
        
        # now we have three possibilities, depending on what's in the output
        # first, check for an error such as "No CUDA Devices found"
        if output.rfind(errStr) > -1:
            logging.error(output)
        elif output.rfind(loseStr) > -1:
            logging.debug("GPU Crack Failed")
            # find the last attempted password
            a = output.rfind(lastPwStr) + len(lastPwStr)
            z = output.find('\n', a)
            lastPw = output[a:z] # not calling strip() here requires patched gpucrack
            logging.debug('lastPw: '+lastPw)
            setStateById(id, state_P2LOST, lastPw)
        else:
            logging.debug("GPU Crack Succeeded")
            # find the cracked password
            a = output.rfind(winStr) + len(winStr)
            z = output.find(' ', a)
            crackedPw = output[a:z].strip()
            logging.debug('crackedPw: '+crackedPw)
            setClearStateByHash(hash, crackedPw, state_P2WON)
    
        fdouterr.close()
        fdin.close()
    
    except:
        logging.debug( formatExceptionInfo() )
        
        
def jabbercrackyMain():
    global config,conn
    config = ConfigParser.RawConfigParser()
    config.read('/etc/jabbercracky.conf')
    conn = None

    maxProcs = int(config.get('tune', 'max_procs'))         
    pool = Pool(processes=maxProcs)
    logging.debug( "Starting Thread Pool" )
    
    while 1:
        try:
            #(0id,1state,2type,3src_ip,4hash,5clear,6created,7cracked,11lastpw)            
            rows = getByState(state_NEW)        
            for r in rows:
                pool.apply_async(crackWorker, [r[0], r[4], r[2]] )
                setRunningById(r[0])

            # now check for fails from the rainbow tables to feed to the GPU
            grows = getByState(state_P1LOST)
            for t in grows:
                if t[2] == 'md5': # phase 2 is only for md5
                    pool.apply_async(gpuWorker, [t[0], t[4]] )
                    setRunningById(t[0])
                         
            # finally, check for fails from the second phase...
            # they only run for one billion times, then lay up until we pick them up again here
            frows = getByState(state_P2LOST)
            for f in frows:
                if f[2] == 'md5': # phase 2 is only for md5
                    pool.apply_async(gpuWorker, [f[0], f[4], f[11]])
                    setRunningById(f[0])
            
            #logging.debug( 'Sleeping...zzz...' )
            time.sleep(10)  # this loop doesn't need 70% of the CPU
        
        except:
            logging.debug( formatExceptionInfo() )
            exit()

        
if __name__ == '__main__':
    jabbercrackyMain()