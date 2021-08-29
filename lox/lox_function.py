from typing import Any, List
import attr
from environment import Environment
from exceptions import ReturnStmtException
from lox_callable import LoxCallable
from stmt import Function

@attr.s(auto_attribs=True)
class LoxFunction(LoxCallable):
    declaration: Function
    closure: Environment

    def __call__(self, interpreter: "Interpreter", arguments: List[Any]) -> Any:
        environment = Environment(self.closure)
        for param, argument in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, argument)
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnStmtException as e:
            return e.value

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"

    def arity(self) -> int:
        return len(self.declaration.params)