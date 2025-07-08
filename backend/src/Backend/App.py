import sys
import signal
import pytz
from flask import Flask, request
from flask_cors import CORS
from typing import Optional, Iterable, List, Dict, Any, Tuple

import PyUtils as PU

from .constants.EnvironmentModes import EnvironmentModes
from .Config import Config
from .model.RoomService import RoomService
from .model.BookingService import BookingService
from .model.UserService import UserService

class App():
    def __init__(self, env: EnvironmentModes):
        self._isInitalized = False
        self._env = env
        self._app: Optional[Flask] = None
        self._config = Config.load(env)

        self._dbTool = PU.DBTool(self._config.dbSecrets, database = self._config.database, useConnPool = True)
        self._roomService = RoomService(self._dbTool)
        self._bookingService = BookingService(self._dbTool)
        self._userService = UserService(self._dbTool)


    # Reference: See the __call__ operator in app.py of Flask's source code
    #   Needed to be served by some WSGI server
    def __call__(self, environ, start_response) -> Iterable[bytes]:
        return self._app.wsgi_app(environ, start_response)

    @property
    def app(self):
        return self._app
    
    @property
    def env(self):
        return self._env
    
    @property
    def port(self):
        return self._config.port

    def initialize(self):
        if (self._isInitalized):
            return
        
        self._isInitalized = True
        self.registerShutdown()

        app = Flask(__name__)
        cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
        app.config['CORS_HEADERS'] = 'Content-Type'

        @app.route('/')
        def index():
            return 'This is the backend server for the room booking app.'
        
        @app.route("/viewAvailableRooms", methods=["GET"])
        def viewAvailableRooms() -> List[Dict[str, Any]]:
            response = []
            db_operation = request.args.get("db_operation")

            if db_operation == "filter":
                roomName = request.args.get("room_name")
                minCapacity = request.args.get("min_capacity")
                maxCapacity = request.args.get("max_capacity")
                startTime = request.args.get("start_time")
                endTime = request.args.get("end_time")
                response = self._roomService.fetchAvailableRooms(roomName, minCapacity, maxCapacity, startTime, endTime)
            else:
                response = self._roomService.fetchAvailableRooms()

            return response
        
        @app.route("/bookRoom", methods=["POST"])
        def bookRoom() -> Tuple[bool, str]:
            data = request.get_json()
            if (not data):
                return [False, "No JSON data received"]

            userId = data.get("user_id")
            roomId = data.get("room_id")
            startDateTimeStr = data.get("start_time")
            endDateTimeStr = data.get("end_time")
            participants = data.get("participants")

            try:
                startDateTime = PU.DateTimeTool.strToDateTime(f"{startDateTimeStr}", tzinfo = pytz.utc)
            except ValueError:
                return [False, "Invalid datetime format for the start datetime"]

            try:
                endDateTime = PU.DateTimeTool.strToDateTime(f"{endDateTimeStr}", tzinfo = pytz.utc)
            except ValueError:
                return [False, "Invalid datetime format for the end datetime"]

            success, msg, bookingId = self._bookingService.bookRoom(userId, roomId, startDateTime, endDateTime, participants)
            return [success, msg]
        
        @app.route("/cancelBooking", methods=["POST"])
        def cancelBooking():
            data = request.get_json()
            if (not data):
                return [False, "No JSON data received"]

            bookingId = data.get("booking_id")
            userId = data.get("user_id")

            return self._bookingService.cancelBooking(bookingId, userId)

        @app.route("/signup", methods=["POST"])
        def signup():
          data = request.get_json()
          print("––––––––––––")
          print("RECEIVED IN SIGNUP")
          print(data)
          print("––––––––––––")
                    
          return self._userService.signup(data["username"], data["email"], data["password"])
      
        @app.route("/login", methods=["POST"])
        def login():
          data = request.get_json()
          print("––––––––––––")
          print("RECEIVED IN LOGIN")
          print(data)
          print("––––––––––––")
                    
          return self._userService.login(data["username"], data["password"])

        self._app = app
        return app

    def shutdown(self, sig: Optional[int] = None, frame: Optional[int] = None):
        self._dbTool.closeDBPools()
        sys.exit(0)

    def registerShutdown(self):
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

    def run(self, *args, **kwargs):
        self._app.run(*args, port = self.port, **kwargs)