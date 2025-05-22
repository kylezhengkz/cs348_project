import os
from dotenv import load_dotenv
from typing import Optional


# DBSecrets: Class to hold the secrets for the databases server
class DBSecrets():
    def __init__(self, db: str = "", username: str = "", password: str= "", host: str = "", port: str = ""):
        self.db = db
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    # load(envPath): Loads the database secreets from a .env environment variable file
    @classmethod
    def load(cls, envPath: Optional[str] = None):
        if (envPath is None):
            envPath = ".env"

        load_dotenv(dotenv_path = envPath)

        db = os.getenv("DATABASE")
        username = os.getenv("DBUSERNAME")
        password = os.getenv("DBPASSWORD")
        host = os.getenv("HOST")
        port = os.getenv("PORT")
        return cls(db, username, password, host, port)