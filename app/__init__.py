from flask import Flask, request, render_template, \
            url_for, jsonify, Response, redirect, send_file, g
import logging
from logging import getLogger, getLevelName, Formatter, StreamHandler
import time
#from gevent import time
from datetime import datetime
# from app import announce
# from app.announce import format_sse #announcer
import gevent
import gevent.queue
from gevent.pywsgi import WSGIServer
# from gevent import monkey
# monkey.patch_all()
from flask_sse import sse


import pika
import queue
import os
import threading
from multiprocessing import current_process
from threading import current_thread


import socket


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('app created')
app.config["REDIS_URL"] = "redis://localhost"   #192.168.88.233:32768
app.register_blueprint(sse, url_prefix='/api/sse_stream')


message_queue = queue.Queue()
gevent_queue = gevent.queue.Queue()


@app.route('/')
def index():
    app.logger.debug('def index():')
    return render_template('index.html')


@app.route('/api/sse')
def apisse():
    app.logger.debug("enter api SSE: ")
    app.logger.debug("message_queue: " + message_queue.__repr__())
    app.logger.debug("gevent_queue: " + gevent_queue.__repr__())
    pid = os.getpid()
    thread_name = current_thread().name
    process_name = current_process().name
    app.logger.debug(f"pid = {pid} - {process_name} - {thread_name}")

    sse.publish({"message": "Hello!"}, type='greeting')
    return '', 204




# we recieve post request and writing data to file. responding is just echo
@app.route('/api/call', methods=['GET', 'POST'])
def apicall():
    if request.method == 'GET':
        return jsonify("/api/call GET: nothing to do ")

    elif request.method == 'POST':
        data = request.get_json()['text'] #just because text field is sent from the client
        sse.publish({"message": str(data)}, type='greeting')
        return jsonify("/api/call POST", data)

    else:
        pass
    return jsonify("/api/call its not GET or POST request!!")
    # return '', 204


@app.route('/api/cpubound')
def cpubound():
    # i7-8700k deals with it in  12.82s with debug range(1000, 16000)
    start_time = time.perf_counter()
    for num in range(1000, 16000):
        get_prime_numbers(num)
    # for num in range(1000, 16000):
    #     get_prime_numbers(num)
    # for num in range(1000, 16000):
    #     get_prime_numbers(num)
    end_time = time.perf_counter()

    app.logger.debug(f"api/cpubound : Elapsed run time: {end_time - start_time} seconds")
    # with open(file_path, 'a') as f:
    #     f.write(f"api/cpubound : Elapsed run time: {end_time - start_time} seconds" + '\n')
    return render_template('cpubound.html', timedelta=end_time - start_time)


# @app.route('/download')
# def download():
#     path = 'file'
#     return send_file(path, as_attachment=True)


def get_prime_numbers(num):
    # cpu-bound

    pid = os.getpid()
    thread_name = current_thread().name
    process_name = current_process().name
    app.logger.debug(f"{pid} - {process_name} - {thread_name}")

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


def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    # print(msg)
    if event is not None:
        msg = f'event: {event}\n{msg}\n\n'
    return msg