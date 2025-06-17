import signal
import sys
from flask import Flask, request
from flask_cors import CORS
from typing import Optional, Iterable

from .constants.EnvironmentModes import EnvironmentModes
from .Config import Config
from .model.RoomService import RoomService
from .constants.Paths import UtilsPath

sys.path.insert(1, UtilsPath)

from PyUtils import DBTool


class App():
    def __init__(self, env: EnvironmentModes):
        self._env = env
        self._app: Optional[Flask] = None
        self._config = Config.load(env)

        self._dbTool = DBTool(self._config.dbSecrets, database = self._config.database, useConnPool = True)
        self._roomService = RoomService(self._dbTool)


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
        self.registerShutdown()

        app = Flask(__name__)
        cors = CORS(app)
        app.config['CORS_HEADERS'] = 'Content-Type'

        @app.route('/')
        def index():
            return 'This is the backend server for the room booking app.'
        
        @app.route("/viewAvailableRooms", methods=["GET", "POST"])
        def view():
            response = []
            if request.method == "GET":
                db_operation = request.args.get("db_operation")

                if db_operation == "filter":
                    roomName = request.args.get("room_name", None)
                    minCapacity = request.args.get("min_capacity", None)
                    maxCapacity = request.args.get("max_capacity", None)
                    startTime = request.args.get("start_time", None)
                    endTime = request.args.get("end_time", None)
                    response = self._roomService.fetchAvailableRooms(roomName, minCapacity, maxCapacity, startTime, endTime)
                else:
                    response = self._roomService.fetchAvailableRooms()

            return response
        
        self._app = app
        return app
    
    #TODO: Implement any cleaning procedures once the backend shutsdown
    def shutdown(self, sig: Optional[int] = None, frame: Optional[int] = None):
        sys.exit(0)

    def registerShutdown(self):
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

    def run(self, *args, **kwargs):
        self._app.run(*args, port = self.port, **kwargs)