from typing import Any, List
import attr
from clock import Clock
from environment import Environment
from exceptions import BreakStmtException, LoxRuntimeError, ReturnStmtException
from expr import Assign, Binary, Call, Expr, Grouping, Literal, Logical, Unary, ExprVisitor, Variable
from lox_callable import LoxCallable
from lox_function import LoxFunction
from stmt import Block, Break, Expression, Function, If, Print, Return, Stmt, StmtVisitor, Var, While
from token_type import TokenType
from tokens import Token

@attr.s(auto_attribs=True)
class Interpreter(ExprVisitor[Any], StmtVisitor[None]):
    lox_globals = Environment(values={"clock": Clock()})
    environment = lox_globals

    def interpret(self, statements: List[Stmt], repl: bool):
        # chapter 8 challenge 1 allow REPL to print last expression
        if repl and isinstance(statements[-1], Expression):
            statements[-1] = Print(statements[-1].expression)
        for statement in statements:
            self.execute(statement)

    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def execute_block(self, statements: List[Stmt], environment: Environment):
        previous = self.environment
        self.environment = environment
        try:
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visit_block_stmt(self, stmt: Block):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_break_stmt(self, stmt: Break):
        raise BreakStmtException

    def visit_expression_stmt(self, stmt: Expression):
        self.evaluate(stmt.expression)

    def visit_function_stmt(self, stmt: Function):
        fn = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, fn)

    def visit_if_stmt(self, stmt: If):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch != None:
            self.execute(stmt.else_branch)

    def visit_print_stmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visit_return_stmt(self, stmt: Return):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise ReturnStmtException(value)

    def visit_var_stmt(self, stmt: Var):
        # chapter 8 challenge 2
        # runtime error to access uninitialized variable
        value = self.environment.nil
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visit_while_stmt(self, stmt: While):
        try:
            while self.is_truthy(self.evaluate(stmt.condition)):
                self.execute(stmt.body)
        except BreakStmtException:
            pass

    def visit_assign_expr(self, expr: Assign) -> Any:
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

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
            raise LoxRuntimeError(expr.operator, "Operands must be two numbers or two strings.")
        if expr.operator.token_type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            # chapter 7 challenge 3 detect and report div by 0 errors
            if right == 0:
                raise LoxRuntimeError(expr.operator, "Cannot divide by zero.")
            return float(left) / float(right)
        if expr.operator.token_type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
    
    def visit_call_expr(self, expr: Call) -> Any:
        callee = self.evaluate(expr.callee)
        arguments: List[Any] = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))
        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")
        if len(arguments) != callee.arity():
            raise LoxRuntimeError(expr.paren, f"Expected {callee.arity()} arguments but got {len(arguments)}.")
        return callee(self, arguments)

    def visit_grouping(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal) -> Any:
        return expr.value
    
    def visit_logical_expr(self, expr: Logical) -> Any:
        left = self.evaluate(expr.left)
        if expr.operator.token_type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        return self.evaluate(expr.right)

    def visit_unary_expr(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)
        if expr.operator.token_type == TokenType.BANG:
            return not self.is_truthy(right)
        elif expr.operator.token_type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)

    def visit_variable_expr(self, expr: Variable) -> Any:
        return self.environment.get(expr.name)

    def check_number_operand(self, operator: Token, operand: Any):
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(operator, "Operand must be a number.")
    
    def check_number_operands(self, operator: Token, left: Any, right: Any):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers.")

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
