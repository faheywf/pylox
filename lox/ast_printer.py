from stmt import Block, Expression, Function, If, Print, Return, Stmt, StmtVisitor, Var, While
from typing import List
import attr
from expr import Assign, Binary, Call, Expr, Grouping, Literal, Unary, ExprVisitor, Variable
from token_type import TokenType
from tokens import Token


@attr.s(auto_attribs=True)
class AstPrinter(ExprVisitor[str], StmtVisitor[None]):
    def print_statements(self, statements: List[Stmt]):
        for statement in statements:
            self.print_statement(statement)

    def print_statement(self, statement: Stmt):
        statement.accept(self)
        
    def print_expr(self, expr: Expr)-> str:
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: List[Expr])-> str:
        s = f"({name}"
        for expr in exprs:
            s += " "
            s += expr.accept(self)
        s += ")"
        return s

    def visit_block_stmt(self, stmt: Block):
        print("(block:")
        for stmt in stmt.statements:
            self.print_statement(stmt)
        print(")")
    
    def visit_expression_stmt(self, stmt: Expression):
        print(self.print_expr(stmt.expression))

    def visit_function_stmt(self, stmt: Function):
        print(f"(fn {stmt.name.lexeme}({', '.join([param.lexeme for param in stmt.params])})")
        self.print_statements(stmt.body)
        print(")")

    def visit_if_stmt(self, stmt: If):
        print("(if then")
        self.print_statement(stmt.then_branch)
        if stmt.else_branch is not None:
            print("else")
            self.print_statement(stmt.else_branch)
        
    def visit_print_stmt(self, stmt: Print):
        print(self.parenthesize("print", stmt.expression))

    def visit_return_stmt(self, stmt: Return):
        print(self.parenthesize("return", stmt.value))

    def visit_var_stmt(self, stmt: Var):
        if stmt.initializer is not None:
            print(self.parenthesize(f"var: {stmt.name.lexeme} = ", stmt.initializer))
        else:
            print(f"(var: {stmt.name.lexeme} = nil)")

    def visit_while_stmt(self, stmt: While):
        print("(while:")
        print(f"\tcondition: {self.print_expr(stmt.condition)}")
        self.print_statement(stmt.body)
        print(")")

    def visit_assign_expr(self, expr: Assign) -> str:
        print(f"(assign {expr.name.lexeme} = {self.print_expr(expr.value)})")

    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_call_expr(self, expr: Call) -> str:
        return self.parenthesize("call", expr.callee, *expr.arguments)
        
    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)
        
    def visit_unary_expr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_variable_expr(self, expr: Variable) -> str:
        return expr.name.lexeme
