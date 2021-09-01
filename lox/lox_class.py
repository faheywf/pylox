from typing import Any, Dict, List, Optional
from exceptions import LoxRuntimeError
from tokens import Token
from lox_callable import LoxCallable
from lox_function import LoxFunction


class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: Dict[str, LoxFunction]):
        self.name = name
        self.methods = methods

    def __call__(self, interpreter: "Interpreter", arguments: List[Any]):
        instance = LoxInstance(self)
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance)(interpreter, arguments)
        return instance

    def  __str__(self):
        return self.name

    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer is None:
            return 0
        return initializer.arity()

    def find_method(self, name: str) -> Optional[LoxFunction]:
        return self.methods.get(name, None)

class LoxInstance:
    def __init__(self, klass: LoxClass):
        self.klass = klass
        self.fields: Dict[str, Any] = {}

    def __str__(self):
        return f"{self.klass.name} instance"

    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method: LoxFunction = self.klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)
            
        raise LoxRuntimeError(f"Undefined property '{name.lexeme}'.")

    def set(self, name: Token, value: Any):
        self.fields[name.lexeme] = value