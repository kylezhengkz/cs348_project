import signal
import sys
from flask import Flask, render_template, request
from hello_world.db import db_open_connection, db_close_connection, db_populate, db_clear, db_fetch_all, db_fetch_by_name, db_fetch_rooms
from hello_world.db import db_book_room, db_cancel_booking
from datetime import datetime
from typing import Optional

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
    
    @app.route("/view", methods=["GET", "POST"])
    def view():
      response = []
      if request.method == "GET":
        db_operation = request.args.get("db_operation")
        print("DB_OPERATION", db_operation)
        if db_operation == "filter":
          print("CUSTOM FILTER", db_operation)
          roomName = request.args.get("room_name", None)
          minCapacity = request.args.get("min_capacity", None)
          maxCapacity = request.args.get("max_capacity", None)
          startTime = request.args.get("start_time", None)
          endTime = request.args.get("end_time", None)
          response = db_fetch_rooms(roomName, minCapacity, maxCapacity, startTime, endTime)
        else:
          print("NO FILTER PRINT ALL", db_operation)
          response = db_fetch_rooms(None, None, None, None, None)
      # print(response)
      return render_template("view.html", response=response)
    
    @app.route("/book_cancel", methods=["GET", "POST"])
    def book_cancel():
        message = ""
        if request.method == "POST":
            action = request.form.get("action")
        
            if action == "book":
                user_id = request.form.get("user_id")
                room_id = request.form.get("room_id")
                book_date = request.form.get("book_date")
                start_time_str = request.form.get("start_time")
                end_time_str = request.form.get("end_time")
                participants = request.form.get("participants")

                try:
                    start_time = datetime.strptime(f"{book_date} {start_time_str}", "%Y-%m-%d %H:%M")
                    end_time = datetime.strptime(f"{book_date} {end_time_str}", "%Y-%m-%d %H:%M")

                except ValueError:
                    return render_template("book_cancel.html", message="Invalid date or time format.")

                success, message = db_book_room(user_id, room_id, book_date, start_time, end_time, participants)

            elif action == "cancel":
                booking_id = request.form.get("booking_id")
                user_id = request.form.get("user_id")

                success, message = db_cancel_booking(booking_id, user_id)

        return render_template("book_cancel.html", message=message)
    
    return app
  

def app_shutdown(sig: Optional[int] = None, frame: Optional[int] = None):
    try:
        db_close_connection()
    except Exception:
        sys.exit(4)
    else:
        sys.exit(0)

signal.signal(signal.SIGTERM, app_shutdown)
signal.signal(signal.SIGINT, app_shutdown)

app = app_initialize()
if __name__ == "__main__":
    app.run(debug=True)