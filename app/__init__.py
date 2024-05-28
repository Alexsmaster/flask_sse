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
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()


import os
from multiprocessing import current_process
from threading import current_thread

import socket




app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('app created')
log_formatter = Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s [%(threadName)s] ") # I am printing thread id here
console_handler = StreamHandler()
console_handler.setFormatter(log_formatter)
app.logger.addHandler(console_handler)
app.logger.info("Hi, how are you")

file_path='messages.txt'

@app.route('/')
def index():
    app.logger.debug('def index():')
    return render_template('index.html')


@app.route('/api/sse')
def apisse():
    def read_messages():
        known_messages = set()
        while True:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    messages = f.readlines()

                for message in messages:
                    message = message.strip()
                    if message not in known_messages:
                        app.logger.debug(f"New message: {message}")
                        event_data = format_sse(data=('Py|msg: ' + str(message)),
                                                event='message')  # json.dumps(data)
                        yield event_data
                        # event_data = format_sse(data=('/api/callGET ' + str(message)),
                        #                         event='occur')  # json.dumps(data)
                        # yield event_data
                        known_messages.add(message)
                time.sleep(0.01)

    # def events_sse():
    #     messages = announcer.listen()
    #     while True:
    #         msg = messages.get()
    #         app.logger.debug(msg)
    #         yield msg  # blocks until a new message arrives
    app.logger.debug('/api/sse started')
    # return Response(events_sse(), content_type='text/event-stream')

    resp = Response(
        read_messages(),
        mimetype='text/event-stream'
    )
    # resp.headers['X-Accel-Buffering'] = 'no'
    # resp.headers['Cache-Control'] = 'no-cache'
    return resp

    #return Response(read_messages(), content_type='text/event-stream')

# we recieve post request and writing data to file. responding is just echo
@app.route('/api/call', methods=['GET', 'POST'])
def apicall():
    if request.method == 'GET':
        return jsonify("/api/call GET: nothing to do ")
    elif request.method == 'POST':
        data = request.get_json()['text'] #just because text field is sent from the client
        # app.logger.debug(data)
        with open(file_path, 'a') as f:
            f.write(data + '\n')
        return jsonify("/api/call POST", data)
    else:
        pass
    return jsonify("/api/call its not GET or POST request!!")
    # return '', 204


@app.route('/api/cpubound')
def cpubound():
    # i7-8700k deals with it in  12.82s with debug
    start_time = time.perf_counter()
    for num in range(1000, 16000):
    #     get_prime_numbers(num)
    # for num in range(1000, 16000):
        get_prime_numbers(num)
    end_time = time.perf_counter()

    app.logger.debug(f"api/cpubound : Elapsed run time: {end_time - start_time} seconds")
    return '', 204


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