from typing import Any, Dict, Optional
import attr
from exceptions import LoxRuntimeError
from tokens import Token

@attr.s(auto_attribs=True)
class Environment:
    enclosing: Optional["Environment"] = None
    values: Dict[str, Any] = {}
    # chapter 8 challenge 2
    # runtime error to access uninitialized variable
    # create a unique instance to represent Nil separately from None
    nil: Any = object()

    def define(self, name: str, value: Any):
        self.values[name] = value

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            # chapter 8 challenge 2
            # runtime error to access uninitialized variable
            if self.values[name.lexeme] is self.nil:
                raise LoxRuntimeError(name, f"Uninitialized variable '{name.lexeme}'.")
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: Any):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")