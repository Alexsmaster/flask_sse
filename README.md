# Flask_sse_websockets
Sample server for alerting clients with minimal delay.

# Install
## install with python, git
sudo apt install git python3.10-venv redis-server -y
## install only redis 
sudo apt install redis-server -y


git clone https://github.com/Alexsmaster/flask_sse.git
cd flask_sse  
git checkout with-redis
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# The Way to run that
cd ~/PycharmProjects/flask_sse/ && source venv/bin/activate  
or  
cd ~/flask_sse && source venv/bin/activate  

in a separate terminals  
1) rq worker app-tasks  
2) web server  
2.a) gunicorn 'app:app'  
2.b) flask run  


Open your web browser, and visit 127.0.0.1:5000.  
Your web browser will automatically connect to the server-sent event stream.  




# tricks for pip 
cat requirements.txt | xargs -n 1 pip install
cat requirements.txt | sed -e '/^\s*#.*$/d' -e '/^\s*$/d' | xargs -n 1 pip install