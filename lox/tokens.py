from typing import Any
import attr
from token_type import TokenType


@attr.s(auto_attribs=True)
class Token:
    token_type: TokenType
    lexeme: str
    literal: Any
    line: int

    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal}"