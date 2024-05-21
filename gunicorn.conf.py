import multiprocessing

bind = "0.0.0.0:8000"
workers = 5 #multiprocessing.cpu_count() * 2 + 1
threads = 10
GEVENT_MONITOR_THREAD_ENABLE = True
monitor_thread = True
TIMEOUT=120