import multiprocessing
import os


#bind = '127.0.0.1:8002'
bind = "0.0.0.0:5000"
workers = 3
backlog = 2048
worker_class = "gevent"
debug = True
reload = True
proc_name = 'gunicorn.proc'
pidfile = '/tmp/gunicorn.pid'
#logfile = 'debug.log'
logfile = 'log.txt'
loglevel = 'debug'

# GEVENT_MONITOR_THREAD_ENABLE = True
# monitor_thread = True
TIMEOUT = 5
