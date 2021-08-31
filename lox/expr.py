from abc import ABC
from typing import Any, Generic, List, Optional, TypeVar
from tokens import Token

R = TypeVar("R")

class Expr(ABC):
	def __init__(self):
		pass
		raise NotImplemented()
	def accept(self, visitor: "ExprVisitor"):
		raise NotImplemented()


class Assign(Expr):
	def __init__(self, name: Token, value: Expr):
		self.name = name
		self.value = value

	def accept(self, visitor: "ExprVisitor[R]") -> R:
		return visitor.visit_assign_expr(self)


class Binary(Expr):
	def __init__(self, left: Expr, operator: Token, right: Expr):
		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor: "ExprVisitor[R]") -> R:
		return visitor.visit_binary_expr(self)


class Call(Expr):
	def __init__(self, callee: Expr, paren: Token, arguments: List[Expr]):
		self.callee = callee
		self.paren = paren
		self.arguments = arguments

	def accept(self, visitor: "ExprVisitor[R]") -> R:
		return visitor.visit_call_expr(self)


class Grouping(Expr):
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor: "ExprVisitor[R]") -> R:
		return visitor.visit_grouping_expr(self)


class Literal(Expr):
	def __init__(self, value: Any):
		self.value = value

	def accept(self, visitor: "ExprVisitor[R]") -> R:
		return visitor.visit_literal_expr(self)


class Logical(Expr):
	def __init__(self, left: Expr, operator: Token, right: Expr):
		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor: "ExprVisitor[R]") -> R:
		return visitor.visit_logical_expr(self)


class Unary(Expr):
	def __init__(self, operator: Token, right: Expr):
		self.operator = operator
		self.right = right

	def accept(self, visitor: "ExprVisitor[R]") -> R:
		return visitor.visit_unary_expr(self)


class Variable(Expr):
	def __init__(self, name: Token):
		self.name = name

	def accept(self, visitor: "ExprVisitor[R]") -> R:
		return visitor.visit_variable_expr(self)


class ExprVisitor(ABC, Generic[R]):
	def visit_assign_expr(self, expr: Assign) -> R:
		raise NotImplemented()

	def visit_binary_expr(self, expr: Binary) -> R:
		raise NotImplemented()

	def visit_call_expr(self, expr: Call) -> R:
		raise NotImplemented()

	def visit_grouping_expr(self, expr: Grouping) -> R:
		raise NotImplemented()

	def visit_literal_expr(self, expr: Literal) -> R:
		raise NotImplemented()

	def visit_logical_expr(self, expr: Logical) -> R:
		raise NotImplemented()

	def visit_unary_expr(self, expr: Unary) -> R:
		raise NotImplemented()

	def visit_variable_expr(self, expr: Variable) -> R:
		raise NotImplemented()

