from flask import Flask, request, render_template, url_for, jsonify, Response, redirect, send_file
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import time
from datetime import datetime
# from app import announce
from app.announce import announcer, format_sse, json


app = Flask(__name__)
app.config['DEBUG'] = True
app.logger.setLevel(logging.INFO)
app.logger.debug('DEBUG in root : 00 event')


@app.route('/')
def index():
    app.logger.info('This is an INFO message')
    app.logger.debug('This is a DEBUG message')
    app.logger.warning('This is a WARNING message')
    app.logger.error('This is an ERROR message')
    app.logger.critical('This is a CRITICAL message')
    app.logger.exception('An exception occurred during a request.')

    return render_template('index.html')


@app.route('/api/sse', methods=['GET', 'POST'])
def apisse():
    app.logger.debug('DEBUG in function apisse : 01 event')
    if request.headers.get('accept') == 'text/event-stream':
        def events_sse():
            app.logger.debug('DEBUG in function apisse : 02 event')
            messages = announcer.listen()
            while True:
                if not messages.empty():
                    app.logger.debug('DEBUG in function apisse : 03 event')
                    msg = messages.get()
                    yield msg    # blocks until a new message arrives
                    time.sleep(0.1)
        return Response(events_sse(), content_type='text/event-stream')
    return redirect("/")




@app.route('/download')
def download():
    path = 'file'
    return send_file(path, as_attachment=True)


@app.route('/api/call', methods=['GET', 'POST'])
def apicall():
    if request.method == 'GET':
        data = request.data
        app.logger.debug(data)
        event_data = format_sse(data=f'/api/call {data}')  # json.dumps(data)
        app.logger.debug(event_data)
        announcer.announce(msg=event_data)
        return jsonify("Done! /api/call GET")

    elif request.method == 'POST':
        data = request.data
        app.logger.debug(data)
        event_data = format_sse(data=f'/api/call {data}')  # json.dumps(data)
        app.logger.debug(event_data)
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

if __name__ == '__main__':
    app.run('0.0.0.0', 8000, debug=True)
