import FixRaidenBoss2 as FRB
from enum import Enum
from typing import List, Optional, Union, Set

from .EnumAtts import EnumAhoCorasickDFAs


# StrEnum: Enum where values are strings
class StrEnum(Enum):
    def __str__(self) -> str:
        return self.value

    # getAll(): Retrieves the all the enum values
    @classmethod
    def getAll(cls, unique: bool = True) -> Union[List[str], Set[str]]:
        result = []
        for strEnum in cls:
            result.append(strEnum.value)
        
        return list(set(result)) if (unique) else result
    
    # _buildAhocorasickDFA(): Builds the DFA for Ahocorasick
    @classmethod
    def _buildAhocorasickDFA(cls):
        data = {}
        for strEnum in cls:
            data[strEnum.value] = strEnum

        result = FRB.AhoCorasickBuilder().build(data = data)
        EnumAhoCorasickDFAs[cls] = result

        return result
    
    # match(name): Searches for an exact match for a particular enum value
    @classmethod
    def match(cls, name: str) -> Optional["StrEnum"]:
        ahoCorasickDFA = EnumAhoCorasickDFAs.get(cls)
        if (ahoCorasickDFA is None):
            cls._buildAhocorasickDFA()

        ahoCorasickDFA = EnumAhoCorasickDFAs[cls]
        return ahoCorasickDFA.getKeyVal(name, errorOnNotFound = False)
    
    # find(txt): Searches whether a particular enum value is contained in 'txt'
    @classmethod
    def find(cls, txt: str) -> Optional["StrEnum"]:
        ahoCorasickDFA = EnumAhoCorasickDFAs.get(cls)
        if (ahoCorasickDFA is None):
            cls._buildAhocorasickDFA()

        ahoCorasickDFA = EnumAhoCorasickDFAs[cls]
        keyword, val = ahoCorasickDFA.get(txt, errorOnNotFound = False)
        return val