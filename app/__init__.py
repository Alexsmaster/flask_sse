from flask import Flask, request, render_template, \
            url_for, jsonify, Response, redirect, send_file, g
import logging
from logging import getLogger, getLevelName, Formatter, StreamHandler
import time
# from gevent import time
from datetime import datetime
from app import announce
from app.announce import announcer, format_sse, json
import gevent
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()


import os
from multiprocessing import current_process
from threading import current_thread




app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('app created')
log_formatter = Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s [%(threadName)s] ") # I am printing thread id here
console_handler = StreamHandler()
console_handler.setFormatter(log_formatter)
app.logger.addHandler(console_handler)
app.logger.info("Hi, how are you")

global messages



@app.route('/')
def index():
    app.logger.debug('def index():')
    return render_template('index.html')


@app.route('/api/sse')
def apisse():
    def events_sse():
        messages = announcer.listen()
        while True:
            msg = messages.get()
            app.logger.debug(msg)
            yield msg  # blocks until a new message arrives
    app.logger.debug('/api/sse started')
    return Response(events_sse(), content_type='text/event-stream')


@app.route('/api/call', methods=['GET', 'POST'])
def apicall():
    if request.method == 'GET':
        # app.logger.debug('apicall GET ')
        data = 'Method _ GET'
        event_data = format_sse(data=('/api/callGET ' + str(data)), event='somekindof event _ api call GET')  # json.dumps(data)
        announcer.announce(msg=event_data)
        return jsonify("Done! /api/callGET")

    elif request.method == 'POST':
        data = request.data
        # app.logger.debug('apicall POST')
        # app.logger.debug(data)
        event_data = format_sse(data=('/api/callPOST ' + str(data)), event='somekindof event _ api call POST')   # json.dumps(data)
        announcer.announce(msg=event_data)
        return jsonify("Done! /api/callPOST")
    else:
        pass
    return jsonify("/api/call if wasnt fired!!")
    # return '', 204




@app.route('/counter')
def counter():
    while True:
        if (time.time() % 1) == 0:
            event_data = format_sse(data=f'/api/call {time.time()}')  # json.dumps(data)
            # app.logger.debug(event_data)
            announcer.announce(msg=event_data)
            time.sleep(0.9)
    return '', 200


@app.route('/download')
def download():
    path = 'file'
    return send_file(path, as_attachment=True)


@app.route('/looper/<int_numb>')
def looper(int_numb):
    primenumbers = get_prime_numbers(int(int_numb))
    event_data = format_sse(data=f'/looper {primenumbers}')
    announcer.announce(msg=event_data)
    return '', 200


# @app.route("/stream")
# def stream():
#     def eventStream():
#         while True:
#             # Poll data from the database
#             # and see if there's a new message
#             if len(messages) > len(previous_messages):
#                 yield "data:
#                 {}\n\n
#                 ".format(messages[len(messages)-1)])"
#
#
#     return Response(eventStream(), mimetype="text/event-stream")



# @app.route('/api/v1/stream')
# def apistream():
#     app.logger.debug('def apistream():')
#     if request.headers.get('accept') == 'text/event-stream':
#         def stream():
#             messages = announcer.listen()  # returns a queue.Queue
#             while True:
#                 msg = messages.get()  # blocks until a new message arrives
#                 yield msg
#         def events():
#             while True:
#                 # yield f"data: {datetime.now()}\n\n"
#                 yield f"data: hi - 1\n\n"
#                 time.sleep(100)
#                 yield f"data: hi - 2\n\n"
#         return Response(stream(), content_type='text/event-stream')
#
#     return redirect("/")

# if __name__ == '__main__':
#     app.run('0.0.0.0', 8000, debug=True)


    # app.logger.info('This is an INFO message')
    # app.logger.debug('This is a DEBUG message')
    # app.logger.warning('This is a WARNING message')
    # app.logger.error('This is an ERROR message')
    # app.logger.critical('This is a CRITICAL message')
    # app.logger.exception('An exception occurred during a request.')

def get_prime_numbers(num):
    # cpu-bound

    pid = os.getpid()
    thread_name = current_thread().name
    process_name = current_process().name
    print(f"{pid} - {process_name} - {thread_name}")

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

    return numbers[-10:]