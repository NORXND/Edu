from flask import Flask
from threading import Thread
from os import environ

"""
    Jest potrzebny np. do Teams
"""

app = Flask(__name__)


@app.route('/ping')
def ping():
    return "pong"


def run_server():
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, host='0.0.0.0', port=int(environ.get('PORT', 5000)))


def init():
    server_thread = Thread(target=run_server)
    server_thread.start()
