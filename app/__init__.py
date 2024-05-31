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





#rabbitmq sender env
# logging.basicConfig()
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@192.168.33.60/%2f')
params = pika.URLParameters(url)
params.socket_timeout = 5
#rabbitmq sender env


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
    pid = os.getpid()
    thread_name = current_thread().name
    process_name = current_process().name
    app.logger.debug(f"pid = {pid} - {process_name} - {thread_name}")


    def events_sse():


        connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.33.60'))

        channel = connection.channel()

        channel.exchange_declare(exchange='sse_events', exchange_type='fanout')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        app.logger.debug("rabbitMQ Queue name: " + queue_name)
        channel.queue_bind(exchange='sse_events', queue=queue_name)

        # def callback(ch, method, properties, body):
        #     yield format_sse(str(body))



        while True:
            method_frame, header_frame, body = channel.basic_get(queue_name)
            if method_frame:
                app.logger.debug("rabbitMQ Queue name: " + queue_name + " With: " + str(method_frame) + " ; " + str(header_frame) + " : " + str(body))
                channel.basic_ack(method_frame.delivery_tag)
                yield format_sse("Q:" + queue_name + str(body))
                # channel.basic_ack(method_frame.delivery_tag)
            else:
                app.logger.debug("Q:" + queue_name + ' No message returned')
                yield format_sse("Q:" + queue_name + ' No message returned')
            # msg = gevent_queue.get(block=True, timeout=10)
            # channel.basic_get(
            #     queue=queue_name, callback=callback, auto_ack=True)
            time.sleep(0.05)


    app.logger.debug('/api/sse started')
    resp = Response(
        events_sse(),
        mimetype='text/event-stream'
    )
    resp.headers['X-Accel-Buffering'] = 'no'
    resp.headers['Cache-Control'] = 'no-cache'
    return resp




# we recieve post request and writing data to file. responding is just echo
@app.route('/api/call', methods=['GET', 'POST'])
def apicall():
    if request.method == 'GET':
        return jsonify("/api/call GET: nothing to do ")

    elif request.method == 'POST':
        data = request.get_json()['text'] #just because text field is sent from the client
        # app.logger.debug(data)
        # with open(file_path, 'a') as f:
        #     f.write(data + '\n')



        connection_sender = pika.BlockingConnection(params)  # Connect to CloudAMQP
        channel_sender = connection_sender.channel()  # start a channel
        # channel_sender.queue_declare(queue='pdfprocess')  # Declare a queue
        channel_sender.exchange_declare(exchange='sse_events',
                                 exchange_type='fanout')

        # Message to send to rabbitmq
        bodys = 'data ke ' + data #str()
        channel_sender.basic_publish(exchange='sse_events', routing_key='', body=bodys)
        connection_sender.close()

        gevent_queue.put(data)
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
    for num in range(1000, 16000):
        get_prime_numbers(num)
    for num in range(1000, 16000):
        get_prime_numbers(num)
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