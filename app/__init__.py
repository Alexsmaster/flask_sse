from flask import Flask, request, render_template, url_for, jsonify, Response, redirect, send_file
import logging
import time
from datetime import datetime
from app import announce
from app.announce import announcer, format_sse, json
# import gevent
# from gevent.pywsgi import WSGIServer
# from gevent import monkey
# monkey.patch_all()


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('app created')


def events_sse():
    messages = announcer.listen()
    while True:
        if not messages.empty():  # and (time.time() % 1) <= 0.05
            app.logger.debug(messages.qsize())
            msg = messages.get()
            yield msg  # blocks until a new message arrives
            time.sleep(0.2)

@app.route('/')
def index():
    app.logger.debug('index rendered')
    # app.logger.info('This is an INFO message')
    # app.logger.debug('This is a DEBUG message')
    # app.logger.warning('This is a WARNING message')
    # app.logger.error('This is an ERROR message')
    # app.logger.critical('This is a CRITICAL message')
    # app.logger.exception('An exception occurred during a request.')

    return render_template('index.html')


@app.route('/api/sse')
def apisse():
    app.logger.debug('apisse started')

    return Response(events_sse(), content_type='text/event-stream')


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

@app.route('/counter')
def counter():
    while True:
        if (time.time() % 1) == 0:
            event_data = format_sse(data=f'/api/call {time.time()}')  # json.dumps(data)
            app.logger.debug(event_data)
            announcer.announce(msg=event_data)
            time.sleep(0.9)


@app.route('/download')
def download():
    path = 'file'
    return send_file(path, as_attachment=True)



@app.route('/api/call', methods=['GET', 'POST'])
def apicall():
    if request.method == 'GET':
        app.logger.debug('apicall GET ')
        data = 'Method _ GET'
        event_data = format_sse(data=f'/api/call {data}')  # json.dumps(data)
        announcer.announce(msg=event_data)
        return jsonify("Done! /api/call GET")

    elif request.method == 'POST':
        data = request.data
        # app.logger.debug('apicall POST')
        # app.logger.debug(data)
        event_data = format_sse(data=f'/api/call {data}')  # json.dumps(data)
        announcer.announce(msg=event_data)
        return jsonify("Done! /api/call POST")
    else:
        pass
    return jsonify("/api/call if wasnt fired!!")
    # return '', 204






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
