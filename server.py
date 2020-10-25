from flask import Flask
from threading import Thread

"""
    Jest potrzebny np. do Teams
"""

app = Flask(__name__)


@app.route('/ping')
def ping():
    return "pong"


def run_server():
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)


def init():
    server_thread = Thread(target=run_server)
    server_thread.start()
