import multiprocessing

bind = "0.0.0.0:8000"
workers = 2 #multiprocessing.cpu_count() * 2 + 1
GEVENT_MONITOR_THREAD_ENABLE = True
monitor_thread = True
TIMEOUT=120