from flask import Flask, render_template
from flask_sse import sse
import time

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/hello')
def publish_hello():
    sse.publish({"message": "Hello!"}, type='greeting')
    return "Message sent!"

# Function to create heavy CPU load
def heavy_task(delay=5):
    # Simulating heavy CPU load
    time.sleep(delay)
    # for _ in range(int(delay)):
    #     time.sleep(1)

# Route to initiate heavy CPU load
@app.route('/heavy_task')
def heavy_task_route():
    # Starting heavy task in a separate process
    heavy_task()
    return "Heavy task initiated."