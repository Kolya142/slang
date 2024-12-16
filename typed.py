from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

class TokenType(Enum):
    LITERAL = 0
    NUMERIC = 1
    WORD = 2
    SYMBOL = 3

class CommandType(Enum):
    SET = 0
    FUNCTION_DEF = 1
    STATEMENT = 2
    FUNCTION_EXEC = 3
    COMMAND = 4
    WORD = 5

@dataclass
class Token:
    value: str
    line: int
    type_: TokenType

@dataclass
class Command:
    type_: CommandType
    args: List[Token | object]

Tokens = List[Token]
Commands = List[Command]
slang_types = {
    "U0": "void",
    "I8": "char",
    "I16": "short",
    "I32": "int",
    "I64": "long long",
    "U8": "unsigned char",
    "U16": "unsigned short",
    "U32": "unsigned int",
    "U64": "unsigned long long",
}
statements = [
    "if",
    "loop"
]
