from abc import ABC
from typing import Any, Generic, List, Optional, TypeVar
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
class Break(Stmt):
	keyword: Token

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_break_stmt(self)


@attr.s(auto_attribs=True)
class Expression(Stmt):
	expression: Expr

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_expression_stmt(self)


@attr.s(auto_attribs=True)
class Function(Stmt):
	name: Token
	params: List[Token]
	body: List[Stmt]

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_function_stmt(self)


@attr.s(auto_attribs=True)
class If(Stmt):
	condition: Expr
	then_branch: Stmt
	else_branch: Optional[Stmt]

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_if_stmt(self)


@attr.s(auto_attribs=True)
class Print(Stmt):
	expression: Expr

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_print_stmt(self)


@attr.s(auto_attribs=True)
class Return(Stmt):
	keyword: Token
	value: Expr

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_return_stmt(self)


@attr.s(auto_attribs=True)
class Var(Stmt):
	name: Token
	initializer: Expr

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_var_stmt(self)


@attr.s(auto_attribs=True)
class While(Stmt):
	condition: Expr
	body: Stmt

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_while_stmt(self)


@attr.s(auto_attribs=True)
class StmtVisitor(ABC, Generic[R]):
	def visit_block_stmt(self, stmt: Block) -> R:
		raise NotImplemented()

	def visit_break_stmt(self, stmt: Break) -> R:
		raise NotImplemented()

	def visit_expression_stmt(self, stmt: Expression) -> R:
		raise NotImplemented()

	def visit_function_stmt(self, stmt: Function) -> R:
		raise NotImplemented()

	def visit_if_stmt(self, stmt: If) -> R:
		raise NotImplemented()

	def visit_print_stmt(self, stmt: Print) -> R:
		raise NotImplemented()

	def visit_return_stmt(self, stmt: Return) -> R:
		raise NotImplemented()

	def visit_var_stmt(self, stmt: Var) -> R:
		raise NotImplemented()

	def visit_while_stmt(self, stmt: While) -> R:
		raise NotImplemented()

