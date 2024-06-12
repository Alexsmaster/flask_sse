# broker_url = 'redis://localhost:6379/0'
# result_backend = 'redis://localhost:6379/0'
#from celery import Celery
#
# @celery.task
# def long_running_task():
#     result = cpu_burning_function()
#     return result
#
# task = long_running_task.apply_async()
#
# celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')