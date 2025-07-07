from enum import Enum


class CommandOpts(Enum):
    EnvironmentMode = "--env"
    DBUserName = "--username"
    DBPassword = "--password"
    DBHost = "--host"
    DBPort = "--port"