from rq import get_current_job
import time
from app import cpu_bound_prime_numbers


def example():
    job = get_current_job()
    print('Starting task')
    # for i in range(seconds):
    #     job.meta['progress'] = 100.0 * i / seconds
    #     job.save_meta()
    #     print(i)
    #     time.sleep(1)

    result = cpu_bound_prime_numbers()
    job.meta['progress'] = 100
    job.save_meta()
    print('Task completed')
    return result