from typing import Any
import attr
from tokens import Token

@attr.s(auto_attribs=True)
class BreakStmtException(Exception):
    pass


@attr.s(auto_attribs=True)
class LoxRuntimeError(Exception):
    token: Token
    message: str


@attr.s(auto_attribs=True)
class ParseException(Exception):
    pass

@attr.s(auto_attribs=True)
class ReturnStmtException(Exception):
    value: Any