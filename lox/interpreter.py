from typing import Any
import attr
from expr import Binary, Expr, Grouping, Literal, Unary, Visitor
from token_type import TokenType
from tokens import Token

@attr.s(auto_attribs=True)
class Interpreter(Visitor[Any]):
    def interpret(self, expr: Expr):
        value = self.evaluate(expr)
        print(self.stringify(value))

    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        if expr.operator.token_type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        if expr.operator.token_type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)
        if expr.operator.token_type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        if expr.operator.token_type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        if expr.operator.token_type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        if expr.operator.token_type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        if expr.operator.token_type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        if expr.operator.token_type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) or isinstance(right, str):
                # chapter 7 challenge 2 allow implicit conversion if one is a str
                return str(left) + str(right)
            raise RuntimeError(expr.operator, "Operands must be two numbers or two strings.")
        if expr.operator.token_type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            # chapter 7 challenge 3 detect and report div by 0 errors
            if right == 0:
                raise RuntimeError(expr.operator, "Cannot divide by zero.")
            return float(left) / float(right)
        if expr.operator.token_type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
    
    def visit_grouping(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal) -> Any:
        return expr.value

    def visit_unary_expr(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)
        if expr.operator.token_type == TokenType.BANG:
            return not self.is_truthy(right)
        elif expr.operator.token_type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)

    def check_number_operand(self, operator: Token, operand: Any):
        if isinstance(operand, float):
            return
        raise RuntimeError(operator, "Operand must be a number.")
    
    def check_number_operands(self, operator: Token, left: Any, right: Any):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError(operator, "Operands must be numbers.")

    def is_truthy(self, obj: Any):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return bool(obj)
        return True

    def is_equal(self, obj_a: Any, obj_b: Any) -> bool:
        return obj_a == obj_b

    def stringify(self, obj: Any) -> str:
        if obj is None:
            return "nil"
        if isinstance(obj, float):
            s = str(obj)
            if s.endswith(".0"):
                return s[:-2]
            return s
        return str(obj)


class RuntimeError(Exception):
    def __init__(self, token: Token, msg: str):
        self.token = token
        super().__init__(msg)