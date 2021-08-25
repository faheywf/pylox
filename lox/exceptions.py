import attr
from tokens import Token

@attr.s(auto_attribs=True)
class LoxRuntimeError(Exception):
    token: Token
    message: str


@attr.s(auto_attribs=True)
class ParseException(Exception):
    pass