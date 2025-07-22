import sys
import signal
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Optional, Iterable, List, Dict, Any, Tuple, Union
from datetime import datetime

import PyUtils as PU

from .constants.EnvironmentModes import EnvironmentModes
from .Config import Config
from .model.RoomService import RoomService
from .model.BookingService import BookingService
from .model.UserService import UserService
from .model.DashboardService import DashboardService
from .view.LogView import LogView

class App():
    def __init__(self, env: EnvironmentModes, isDebug: bool = False):
        self._isInitalized = False
        self._env = env
        self._app: Optional[Flask] = None
        self._config = Config.load(env)
        self._isDebug = isDebug

        self._dbTool = PU.DBTool(self._config.dbSecrets, database = self._config.database, useConnPool = True)

        self._logView = LogView(verbose = isDebug)
        self._logView.includePrefix = False

        self._roomService = RoomService(self._dbTool, view = self._logView)
        self._bookingService = BookingService(self._dbTool, view = self._logView)
        self._userService = UserService(self._dbTool, view = self._logView)
        self._dashService = DashboardService(self._dbTool, view = self._logView)


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
    
    @property
    def isDebug(self) -> bool:
        return self._isDebug
    
    @isDebug.setter
    def isDebug(self, newIsDebug: bool):
        self._isDebug = newIsDebug
        self._logView.verbose = newIsDebug

    def print(self, *args, **kwargs):
        self._logView.print(*args, **kwargs)

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
    
        @app.route("/deleteRoom", methods=["POST"])
        def delete():
            data = request.get_json()
            print("RECEIVED IN DELETE", data)
            return self._roomService.deleteRoom(data["roomID"])
        
        @app.route("/bookRoom", methods=["POST"])
        def bookRoom():
            data = request.get_json()

            if not data:
                return jsonify({ "success": False, "message": "No JSON data received" }), 400

            try:
                userId = data.get("user_id")
                roomId = data.get("room_id")
                startDateTimeStr = data.get("start_time")
                endDateTimeStr = data.get("end_time")
                participants = data.get("participants")

                if not all([userId, roomId, startDateTimeStr, endDateTimeStr]):
                    return jsonify({ "success": False, "message": "Missing required fields" }), 400

                start_dt = datetime.fromisoformat(startDateTimeStr)
                end_dt = datetime.fromisoformat(endDateTimeStr)


                # Call booking service
                success, message, bookingId = self._bookingService.bookRoom(userId, roomId, start_dt, end_dt, participants)
                # self.print(" BookingService.bookRoom returned ->", success, message, bookingId)

                return jsonify({
                    "success": success,
                    "message": message,
                    "booking_id": bookingId
                }), 200 if success else 400

            except Exception as e:
                self.print(f" Booking validation failed: {str(e)}")
                return jsonify({
                    "success": False,
                    "message": str(e) or "Booking failed due to an unknown error."
                }), 400

        
        @app.route("/cancelBooking", methods=["POST"])
        def cancelBooking():
            data = request.get_json()
            if not data:
                return jsonify({ "success": False, "message": "No JSON data received" }), 400

            bookingId = data.get("booking_id")
            userId = data.get("user_id")

            try:
                success, message = self._bookingService.cancelBooking(bookingId, userId)
                return jsonify({ "success": success, "message": message }), 200 if success else 400
            except Exception as e:
                self.print(f"CancelBooking error: {str(e)}")
                return jsonify({ "success": False, "message": "Cancellation failed due to server error." }), 500

        
        @app.route("/getFutureBookings", methods=["GET"])
        def getFutureBookings():
            userId = request.args.get("userId")
            self.print(f"[GET] /getFutureBookings - userId: {userId}")
            return self._bookingService.getFutureBookings(userId)

        @app.route("/getBookingsAndCancellations", methods=["GET"])
        def getBookingsAndCancellations():
            userId = request.args.get("userId")
            self.print(f"/getBookingsAndCancellations - userId: {userId}", prefix = "[GET]")
            return self._bookingService.getBookingsAndCancellations(userId)

        @app.route("/signup", methods=["POST"])
        def signup():
            data = request.get_json()
            self.print(f"RECEIVED IN SIGNUP {data}")
                    
            return self._userService.signup(data["username"], data["email"], data["password"])
      
        @app.route("/login", methods=["POST"])
        def login():
            data = request.get_json()
            self.print(f"RECEIVED IN LOGIN {data}")
                    
            return self._userService.login(data["username"], data["password"])
        
        @app.route("/getDashboardMetrics", methods=["GET"])
        def getDashboardMetrics():
            userId = request.args.get("userId")
            self.print(f"/getDashboardMetrics - userId: {userId}", prefix = "[GET]")
            success, result = self._dashService.getDashboardMetrics(userId)
            return jsonify(result), 200 if success else 400
        
        @app.route("/getBookingFrequency", methods=["POST"])
        def getBookingFrequency() -> Tuple[bool, Union[str, List[Dict[str, Any]]]]:
            data = request.get_json()

            userId = data.get("user_id")
            startDateTime = data.get("start_time")
            endDateTime = data.get("end_time")
            queryLimit = data.get("participants")

            try:
                userId  = uuid.UUID(userId)
            except ValueError:
                return [False, "Invalid UUID format for user ID"]
            
            startDateTime = PU.DateTimeTool.strToDateTime(startDateTime)
            endDateTime = PU.DateTimeTool.strToDateTime(endDateTime)
            queryLimit = int(queryLimit)
            
            return self._dashService.getBookingFrequency(userId, startDateTime, endDateTime, queryLimit = queryLimit)


        self._app = app
        return app

    def shutdown(self, sig: Optional[int] = None, frame: Optional[int] = None):
        self._dbTool.closeDBPools()
        sys.exit(0)

    def registerShutdown(self):
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

    def run(self, *args, **kwargs):
        self._app.run(port = self.port, *args, debug = self._isDebug, **kwargs)