import sys
import os
from dotenv import load_dotenv
from typing import Optional

from .constants.Paths import UtilsPath
from .constants.EnvironmentModes import EnvironmentModes

sys.path.insert(1, UtilsPath)

from PyUtils import DBSecrets, Paths


class Config():
    ConfigFuncs = {
        EnvironmentModes.Toy: "loadToy",
        EnvironmentModes.Dev: "loadDev",
        EnvironmentModes.Prod: "loadProd"
    }

    def __init__(self, dbSecrets: DBSecrets, database: str, port: int):
        self.dbSecrets = dbSecrets
        self.database = database
        self.port = port

    @classmethod
    def loadFromFiles(cls, envPublicConfigsFile: str, globalSecretsFile: Optional[str] = None) -> "Config":
        if (globalSecretsFile is None):
            globalSecretsFile = os.path.join(Paths.BackEndFolder.value, ".env")

        dbSecrets = DBSecrets.load(envPath = globalSecretsFile)

        load_dotenv(dotenv_path = envPublicConfigsFile)
        database = os.getenv("DATABASE")
        port = os.getenv("APP_PORT")
        port = int(port)
        
        return cls(dbSecrets, database, port)
    
    @classmethod
    def loadDev(cls) -> "Config":
        envPublicConfigsFile = os.path.join(Paths.BackEndFolder.value, "dev.env")
        return cls.loadFromFiles(envPublicConfigsFile)
    
    @classmethod
    def loadProd(cls) -> "Config":
        envPublicConfigsFile = os.path.join(Paths.BackEndFolder.value, "prod.env")
        return cls.loadFromFiles(envPublicConfigsFile)
    
    @classmethod
    def loadToy(cls) -> "Config":
        envPublicConfigsFile = os.path.join(Paths.BackEndFolder.value, "toy.env")
        return cls.loadFromFiles(envPublicConfigsFile)
    
    @classmethod
    def load(cls, env: EnvironmentModes) -> "Config":
        loadConfigFuncName = cls.ConfigFuncs.get(env)
        if (loadConfigFuncName is None):
            raise KeyError(f"The config load function for the following config ({env.value}) has not been implemented yet")
        
        return getattr(cls, loadConfigFuncName)()