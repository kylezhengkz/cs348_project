import os
from dotenv import load_dotenv
from typing import Optional

from ..constants.Paths import Paths


# DBSecrets: Class to hold the secrets for the databases server
class DBSecrets():
    def __init__(self, username: str = "", password: str= "", host: str = "", port: str = ""):
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    # load(envPath): Loads the database secreets from a .env environment variable file
    @classmethod
    def load(cls, envPath: Optional[str] = None):
        if (envPath is None):
            envPath = os.path.join(Paths.ProjectFolder.value, ".env")

        load_dotenv(dotenv_path = envPath)

        username = os.getenv("DB_USERNAME")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        return cls(username = username, password = password, host = host, port = port)