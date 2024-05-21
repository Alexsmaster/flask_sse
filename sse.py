from flask import Flask, request, render_template, url_for, jsonify, Response, redirect, send_file
import logging
import time
from datetime import datetime
from announce import announcer, format_sse, json



app = Flask(__name__)
app.logger.setLevel(logging.INFO)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1/sse', methods=['GET', 'POST'])
def apisse():
    if request.headers.get('accept') == 'text/event-stream':
        def events_sse():
            messages = announcer.listen()
            while True:
                yield f"data: {datetime.now()}\n\n"
                if not messages.empty():
                    msg = messages.get()
                    yield msg    # blocks until a new message arrives
                    time.sleep(1)
                time.sleep(0.1)

        return Response(events_sse(), content_type='text/event-stream')
    return redirect("/")


@app.route('/api/v1/stream')
def apistream():
    app.logger.debug('def apistream():')
    if request.headers.get('accept') == 'text/event-stream':
        def stream():
            messages = announcer.listen()  # returns a queue.Queue
            while True:
                msg = messages.get()  # blocks until a new message arrives
                yield msg
        def events():
            while True:
                # yield f"data: {datetime.now()}\n\n"
                yield f"data: hi - 1\n\n"
                time.sleep(100)
                yield f"data: hi - 2\n\n"
        return Response(stream(), content_type='text/event-stream')

    return redirect("/")


@app.route('/download')
def download():
    path = 'file'

    return send_file(path, as_attachment=True)


@app.route('/sleep')
def sleepsrv():
    time.sleep(10)
    return '', 204


@app.route('/darov')
def darov():
    data = 'darov'
    event_data = format_sse(data=data)  #json.dumps(data)
    announcer.announce(msg=event_data)
    return '', 204


# app.logger.info('This is an INFO message')
# app.logger.debug('This is a DEBUG message')
# app.logger.warning('This is a WARNING message')
# app.logger.error('This is an ERROR message')
# app.logger.critical('This is a CRITICAL message')
# app.logger.exception('An exception occurred during a request.')