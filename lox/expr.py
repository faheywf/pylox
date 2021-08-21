from abc import ABC
from typing import Any, Generic, TypeVar
import attr
from tokens import Token

R = TypeVar("R")

@attr.s(auto_attribs=True)
class Expr(ABC):
	def accept(self, visitor: "Visitor"):
		raise NotImplemented()


@attr.s(auto_attribs=True)
class Binary(Expr):
	left: Expr
	operator: Token
	right: Expr

	def accept(self, visitor: "Visitor[R]") -> R:
		return visitor.visit_binary_expr(self)


@attr.s(auto_attribs=True)
class Grouping(Expr):
	expression: Expr

	def accept(self, visitor: "Visitor[R]") -> R:
		return visitor.visit_grouping_expr(self)


@attr.s(auto_attribs=True)
class Literal(Expr):
	value: Any

	def accept(self, visitor: "Visitor[R]") -> R:
		return visitor.visit_literal_expr(self)


@attr.s(auto_attribs=True)
class Unary(Expr):
	operator: Token
	right: Expr

	def accept(self, visitor: "Visitor[R]") -> R:
		return visitor.visit_unary_expr(self)


@attr.s(auto_attribs=True)
class Visitor(ABC, Generic[R]):
	def visit_binary_expr(self, expr: Binary) -> R:
		raise NotImplemented()

	def visit_grouping_expr(self, expr: Grouping) -> R:
		raise NotImplemented()

	def visit_literal_expr(self, expr: Literal) -> R:
		raise NotImplemented()

	def visit_unary_expr(self, expr: Unary) -> R:
		raise NotImplemented()

