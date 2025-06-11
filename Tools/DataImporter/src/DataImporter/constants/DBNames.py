from enum import Enum

class DBNames(Enum):
    Toy = "postgres"
    Dev = "development"
    Prod = "production"