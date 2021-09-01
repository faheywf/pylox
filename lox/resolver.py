from typing import Callable, Dict, List, Union
import attr
from class_type import ClassType
from expr import Assign, Binary, Call, Expr, ExprVisitor, Get, Grouping, Literal, Logical, Set, This, Unary, Variable
from function_type import FunctionType
from interpreter import Interpreter
from stmt import Block, Class, Expression, Function, If, Print, Return, Stmt, StmtVisitor, Var, While
from tokens import Token

Scope = Dict[str, bool]
Resolvable = Union[List[Stmt], Stmt, Expr]

@attr.s(auto_attribs=True)
class Resolver(ExprVisitor[None], StmtVisitor[None]):
    interpreter: Interpreter
    report: Callable[[int, str, str], None]
    scopes: List[Scope] = []
    current_function: FunctionType = FunctionType.NONE
    current_class: ClassType = ClassType.NONE

    def resolve(self, resolvable: Resolvable):
        if isinstance(resolvable, List):
            for statement in resolvable:
                self.resolve(statement)
        else:
            resolvable.accept(self)

    def resolve_function(self, function: Function, function_type: FunctionType):
        enclosing_function = self.current_function
        self.current_function = function_type

        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()
        self.current_function = enclosing_function

    def error(self, token: Token, msg: str):
        self.report(token.line, "", msg)

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def peek(self):
        return self.scopes[-1]

    def declare(self, name: Token):
        if not self.scopes:
            return
        scope = self.peek()
        if name.lexeme in scope:
            self.error(name, "Already a variable with this name in this scope.")
        scope[name.lexeme] = False

    def define(self, name: Token):
        if not self.scopes:
            return
        self.peek()[name.lexeme] = True

    def resolve_local(self, expr: Expr, name: Token):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i].keys():
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return
        # i = 0
        # scopes = self.scopes[:]
        # while scopes:
        #     scope = scopes.pop()
        #     if name.lexeme in scope:
        #         self.interpreter.resolve(expr, i)
        #         return
        #     i += 1

    def visit_block_stmt(self, stmt: Block):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()

    def visit_class_stmt(self, stmt: Class):
        enclosing_class: ClassType = self.current_class
        self.current_class = ClassType.CLASS

        self.declare(stmt.name)
        self.define(stmt.name)

        self.begin_scope()
        self.peek()["this"] = True
        for method in stmt.methods:
            if method.name.lexeme == "init":
                declaration = FunctionType.INITIALIZER
            else:
                declaration = FunctionType.METHOD
            
            self.resolve_function(method, declaration)
        self.end_scope()

        self.current_class = enclosing_class

    def visit_expression_stmt(self, stmt: Expression):
        self.resolve(stmt.expression)

    def visit_function_stmt(self, stmt: Function):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.FUNCTION)

    def visit_if_stmt(self, stmt: If):
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)

    def visit_print_stmt(self, stmt: Print):
        self.resolve(stmt.expression)

    def visit_return_stmt(self, stmt: Return):
        if self.current_function == FunctionType.NONE:
            self.error(stmt.keyword, "Can't return from top-level code.")
        if stmt.value is not None:
            if self.current_function == FunctionType.INITIALIZER:
                self.error(stmt.keyword, "Can't return a value from an initializer.")
            self.resolve(stmt.value)

    def visit_var_stmt(self, stmt: Var):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)

    def visit_while_stmt(self, stmt: While):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)

    def visit_assign_expr(self, expr: Assign):
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_binary_expr(self, expr: Binary):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_call_expr(self, expr: Call):
        self.resolve(expr.callee)
        for argument in expr.arguments:
            self.resolve(argument)

    def visit_get_expr(self, expr: Get):
        self.resolve(expr.object)

    def visit_grouping_expr(self, expr: Grouping):
        self.resolve(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return

    def visit_logical_expr(self, expr: Logical):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_set_expr(self, expr: Set):
        self.resolve(expr.value)
        self.resolve(expr.object)

    def visit_this_expr(self, expr: This):
        if self.current_class == ClassType.NONE:
            self.error(expr.keyword, "Can't use 'this' outside of a class.")
        self.resolve_local(expr, expr.keyword)

    def visit_unary_expr(self, expr: Unary):
        self.resolve(expr.right)

    def visit_variable_expr(self, expr: Variable):
        if self.scopes and self.peek().get(expr.name.lexeme, None) is False:
            self.error(expr.name, "Can't read local variable in its own initializer.")
        self.resolve_local(expr, expr.name)

