from enum import Enum
from typing import Optional


class EnvironmentModes(Enum):
    Toy = "toy"
    Dev = "dev"
    Prod = "prod"

    @classmethod
    def find(cls, search: str) -> Optional["EnvironmentModes"]:
        for mode in cls:
            if (search == mode.value):
                return mode

        return None