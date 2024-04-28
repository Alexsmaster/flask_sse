# Flask_sse_websockets
Semple websocket server for alerting clients with minimal delay.


If you are using a Redis server that has a password use:

app.config["REDIS_URL"] = "redis://:password@localhost"

$ gunicorn sse:app --worker-class gevent --bind 127.0.0.1:8000
Open your web browser, and visit 127.0.0.1:8000.  
Your web browser will automatically connect to the server-sent event stream.  
Open another tab, and visit 127.0.0.1:8000/hello.  
You should get a Javascript alert in the first tab when you do so.