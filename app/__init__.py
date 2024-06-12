from flask import Flask, request, render_template, jsonify
import logging
import time
from flask_sse import sse
import os
from multiprocessing import current_process
from threading import current_thread


app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/api/sse_stream')

# app.logger.setLevel(logging.DEBUG)

# pid = os.getpid()
# thread_name = current_thread().name
# process_name = current_process().name
# app.logger.debug(f" app created: pid - {pid}, thread_name - {thread_name}, process_name - {process_name}")


@app.route('/')
def index():
    # app.logger.debug('def index():')
    return render_template('index.html')


@app.route('/api/call', methods=['POST'])
def apicall():
    pid = os.getpid()
    thread_name = current_thread().name
    process_name = current_process().name
    # app.logger.debug(f"cpubound: pid - {pid}, thread_name - {thread_name}, process_name - {process_name}")
    data = request.get_json()['text']
    sse.publish(str(f"pid - {pid}, thread_name - {thread_name}, process_name - {process_name}" + data))
    return jsonify("/api/call POST", data)


@app.route('/api/cpubound')
def cpubound():
    pid = os.getpid()
    thread_name = current_thread().name
    process_name = current_process().name
    app.logger.debug(f"cpubound: pid - {pid}, thread_name - {thread_name}, process_name - {process_name}")
    done_with_thread = f"cpubound: pid - {pid}, thread_name - {thread_name}, process_name - {process_name}"
    result = cpu_bound_prime_numbers()

    return render_template('cpubound.html', timedelta=result, done_with_thread=done_with_thread)


def cpu_bound_prime_numbers():
    start_time = time.perf_counter()
    for num in range(1000, 16000):         # i7-8700k deals with it in  12.82s with debug range(1000, 16000)
        get_prime_numbers(num)
    end_time = time.perf_counter()
    timedelta = end_time - start_time
    app.logger.debug(f" cpu_burning_function : Elapsed run time: {timedelta} seconds")
    return timedelta


def get_prime_numbers(num):
    # cpu-bound
    numbers = []

    prime = [True for i in range(num + 1)]
    p = 2

    while p * p <= num:
        if prime[p]:
            for i in range(p * 2, num + 1, p):
                prime[i] = False
        p += 1

    prime[0] = False
    prime[1] = False

    for p in range(num + 1):
        if prime[p]:
            numbers.append(p)

    return numbers[-1]

