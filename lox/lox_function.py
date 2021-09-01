from typing import Any, List
import attr
from environment import Environment
from exceptions import ReturnStmtException
from lox_callable import LoxCallable
from stmt import Function

class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment, is_initializer: bool):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def __call__(self, interpreter: "Interpreter", arguments: List[Any]) -> Any:
        environment = Environment(self.closure)
        for param, argument in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, argument)
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnStmtException as e:
            if self.is_initializer:
                return self.closure.get_at(0, "this")
            return e.value
        if self.is_initializer:
            return self.closure.get_at(0, "this")

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"

    def arity(self) -> int:
        return len(self.declaration.params)

    def bind(self, instance: "LoxInstance")-> "LoxFunction":
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration, environment, self.is_initializer)