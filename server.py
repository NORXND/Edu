from asyncio import get_event_loop, new_event_loop
from os import environ
from threading import Thread

from botbuilder.schema import Activity
from flask import Flask, request, Response, redirect

from teams_platform.main import api_handler, ADAPTER

app = Flask(__name__)

# Ping
@app.route('/ping')
def ping():
    return "pong"

# Main page
@app.route('/')
def home():
    return redirect("https://norxnd.cal24.pl/edu", code=302)

# Podstawowy endpoint dla Teams
@app.route('/teams/event', methods=['GET', 'POST'])
def teams_event():
    # Pobiera pętle lub ją tworzy.
    try:
        loop = get_event_loop()
    except RuntimeError:
        loop = new_event_loop()
    # Sprawdza, czy dane się zgadzają. Pobiera „body”.
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    # Tworzy model z „body” oraz pobiera „Auth Header”.
    activity = Activity().deserialize(body)
    auth_header = (request.headers["Authorization"] if "Authorization" in request.headers else "")

    # Uruchamia pętle
    loop.run_until_complete(loop.create_task(ADAPTER.process_activity(activity, auth_header, api_handler)))
    return Response(status=201)


def run_server():
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, host='127.168.1.1', port=int(environ.get('PORT', 5000)))


def init():
    server_thread = Thread(target=run_server)
    server_thread.start()


init()
