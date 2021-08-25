from abc import ABC
from typing import Any, Generic, List, TypeVar
import attr
from expr import Expr
from tokens import Token

R = TypeVar("R")

@attr.s(auto_attribs=True)
class Stmt(ABC):
	def accept(self, visitor: "StmtVisitor"):
		raise NotImplemented()


@attr.s(auto_attribs=True)
class Block(Stmt):
	statements: List[Stmt]

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_block_stmt(self)


@attr.s(auto_attribs=True)
class Expression(Stmt):
	expression: Expr

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_expression_stmt(self)


@attr.s(auto_attribs=True)
class Print(Stmt):
	expression: Expr

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_print_stmt(self)


@attr.s(auto_attribs=True)
class Var(Stmt):
	name: Token
	initializer: Expr

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_var_stmt(self)


@attr.s(auto_attribs=True)
class StmtVisitor(ABC, Generic[R]):
	def visit_block_stmt(self, stmt: Block) -> R:
		raise NotImplemented()

	def visit_expression_stmt(self, stmt: Expression) -> R:
		raise NotImplemented()

	def visit_print_stmt(self, stmt: Print) -> R:
		raise NotImplemented()

	def visit_var_stmt(self, stmt: Var) -> R:
		raise NotImplemented()

