from abc import ABC
from typing import Any, List
import attr

@attr.s(auto_attribs=True)
class LoxCallable(ABC):
    def __call__(self, interpreter: "Interpreter", arguments: List[Any]) -> Any:
        raise NotImplemented()

    def arity(self) -> int:
        raise NotImplemented()