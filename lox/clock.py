import time
from typing import Any, List
import attr
from lox_callable import LoxCallable

@attr.s(auto_attribs=True)
class Clock(LoxCallable):
    def __call__(self, interpreter: "Interpreter", arguments: List[Any]) -> Any:
        return time.time()

    def __str__(self):
        return "<native fn>"

    def arity(self) -> int:
        return 0