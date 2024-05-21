# Flask_sse_websockets
Sample server for alerting clients with minimal delay.


# Install
git clone urlofthatrepo
cd flask_sse
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# The Way to run that
cd ~/PycharmProjects/Flask_sse/ && source .venv/bin/activate && gunicorn 'sse:app' --worker-class gevent -b 0.0.0.0:5000 --reload --access-logfile log.txt
gunicorn 'sse:app'  --worker-class sync -b 0.0.0.0:5000 --reload --log-level debug --access-logfile log.txt 

Open your web browser, and visit 127.0.0.1:5000.  
Your web browser will automatically connect to the server-sent event stream.  