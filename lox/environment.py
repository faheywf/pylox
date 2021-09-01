from typing import Any, Dict, Optional, Union
import attr
from exceptions import LoxRuntimeError
from tokens import Token


class Environment:
    def __init__(self, enclosing: Optional["Environment"] = None):
        self.enclosing = enclosing
        self.values = {}
        # chapter 8 challenge 2
        # runtime error to access uninitialized variable
        # create a unique instance to represent Nil separately from None
        self.nil: Any = object()

    def define(self, name: str, value: Any):
        self.values[name] = value

    def ancestor(self, distance: int) -> "Environment":
        environment = self
        for i in range(distance):
            environment = environment.enclosing
        return environment

    def get_at(self, distance: int, name: Union[Token, str]) -> Any:
        ancestor = self.ancestor(distance)
        if isinstance(name, Token):
            key = name.lexeme
        else:
            key = name
        if key in ancestor.values:
            return ancestor.values[key]
        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign_at(self, distance: int, name: Token, value: Any):
        self.ancestor(distance).values[name.lexeme] = value

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