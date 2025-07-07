from enum import Enum


class ShortCommandOpts(Enum):
    EnvironmentMode = "-e"
    DBUserName = "-u"
    DBPassword = "-p"
    DBHost = "-ho"
    DBPort = "-po"