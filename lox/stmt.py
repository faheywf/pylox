from abc import ABC
from typing import Any, Generic, List, Optional, TypeVar
from expr import Expr
from tokens import Token

R = TypeVar("R")

class Stmt(ABC):
	def __init__(self):
		pass
		raise NotImplemented()
	def accept(self, visitor: "StmtVisitor"):
		raise NotImplemented()


class Block(Stmt):
	def __init__(self, statements: List[Stmt]):
		self.statements = statements

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_block_stmt(self)


class Break(Stmt):
	def __init__(self, keyword: Token):
		self.keyword = keyword

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_break_stmt(self)


class Class(Stmt):
	def __init__(self, name: Token, methods: List["Function"]):
		self.name = name
		self.methods = methods

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_class_stmt(self)


class Expression(Stmt):
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_expression_stmt(self)


class Function(Stmt):
	def __init__(self, name: Token, params: List[Token], body: List[Stmt]):
		self.name = name
		self.params = params
		self.body = body

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_function_stmt(self)


class If(Stmt):
	def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Optional[Stmt]):
		self.condition = condition
		self.then_branch = then_branch
		self.else_branch = else_branch

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_if_stmt(self)


class Print(Stmt):
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_print_stmt(self)


class Return(Stmt):
	def __init__(self, keyword: Token, value: Expr):
		self.keyword = keyword
		self.value = value

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_return_stmt(self)


class Var(Stmt):
	def __init__(self, name: Token, initializer: Expr):
		self.name = name
		self.initializer = initializer

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_var_stmt(self)


class While(Stmt):
	def __init__(self, condition: Expr, body: Stmt):
		self.condition = condition
		self.body = body

	def accept(self, visitor: "StmtVisitor[R]") -> R:
		return visitor.visit_while_stmt(self)


class StmtVisitor(ABC, Generic[R]):
	def visit_block_stmt(self, stmt: Block) -> R:
		raise NotImplemented()

	def visit_break_stmt(self, stmt: Break) -> R:
		raise NotImplemented()

	def visit_class_stmt(self, stmt: Class) -> R:
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

