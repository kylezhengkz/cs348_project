import atexit
import signal
import sys
from flask import Flask, render_template, request
from hello_world.db import db_open_connection, db_close_connection, db_populate, db_clear, db_fetch_all, db_fetch_by_name

def app_initialize():
    try:
        db_open_connection()
    except Exception:
        sys.exit(4)
    
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        response = []
        if request.method == "POST":
            db_operation = request.form.get("db_operation")
            if db_operation == "db_populate":
                db_populate()
                response = db_fetch_all()
            elif db_operation == "db_clear":
                db_clear()
                response = db_fetch_all()
            elif db_operation == "db_fetch_by_name":
                response = db_fetch_by_name(request.form.get("db_search_value", "").strip())
        else:
            response = db_fetch_all()
        return render_template("index.html", response=response)
    
    return app

def app_shutdown():
    try:
        db_close_connection()
    except Exception:
        sys.exit(4)

signal.signal(signal.SIGTERM, app_shutdown)
signal.signal(signal.SIGINT, app_shutdown)
atexit.register(app_shutdown)

app = app_initialize()