from enum import Enum
from typing import TypeVar


# GenericTypes: Some common generic types
class GenericTypes(Enum):
    ConfigKey = TypeVar("ConfigKey")