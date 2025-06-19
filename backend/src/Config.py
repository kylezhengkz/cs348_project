import os
from dotenv import load_dotenv
from typing import Optional

import PyUtils as PU

from .constants.EnvironmentModes import EnvironmentModes


class Config():
    ConfigFuncs = {
        EnvironmentModes.Toy: "loadToy",
        EnvironmentModes.Dev: "loadDev",
        EnvironmentModes.Prod: "loadProd"
    }

    def __init__(self, dbSecrets: PU.DBSecrets, database: str, port: int):
        self.dbSecrets = dbSecrets
        self.database = database
        self.port = port

    @classmethod
    def loadFromFiles(cls, envPublicConfigsFile: str, globalSecretsFile: Optional[str] = None) -> "Config":
        if (globalSecretsFile is None):
            globalSecretsFile = os.path.join(PU.Paths.BackEndFolder.value, ".env")

        dbSecrets = PU.DBSecrets.load(envPath = globalSecretsFile)

        load_dotenv(dotenv_path = envPublicConfigsFile)
        database = os.getenv("DATABASE")
        port = os.getenv("APP_PORT")
        port = int(port)
        
        return cls(dbSecrets, database, port)
    
    @classmethod
    def loadDev(cls) -> "Config":
        envPublicConfigsFile = os.path.join(PU.Paths.BackEndFolder.value, "dev.env")
        return cls.loadFromFiles(envPublicConfigsFile)
    
    @classmethod
    def loadProd(cls) -> "Config":
        envPublicConfigsFile = os.path.join(PU.Paths.BackEndFolder.value, "prod.env")
        return cls.loadFromFiles(envPublicConfigsFile)
    
    @classmethod
    def loadToy(cls) -> "Config":
        envPublicConfigsFile = os.path.join(PU.Paths.BackEndFolder.value, "toy.env")
        return cls.loadFromFiles(envPublicConfigsFile)
    
    @classmethod
    def load(cls, env: EnvironmentModes) -> "Config":
        loadConfigFuncName = cls.ConfigFuncs.get(env)
        if (loadConfigFuncName is None):
            raise KeyError(f"The config load function for the following config ({env.value}) has not been implemented yet")
        
        return getattr(cls, loadConfigFuncName)()