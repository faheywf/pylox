from typing import List
import attr
from expr import Binary, Expr, Grouping, Literal, Unary, Visitor
from token_type import TokenType
from tokens import Token


@attr.s(auto_attribs=True)
class AstPrinter(Visitor[str]):
    def print(self, expr: Expr)-> str:
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: List[Expr])-> str:
        s = f"({name}"
        for expr in exprs:
            s += " "
            s += expr.accept(self)
        s += ")"
        return s


    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
        
    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)
        
    def visit_unary_expr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

if __name__ == "__main__":
    expression: Expr = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67))
    )
    ast_printer = AstPrinter()
    print(ast_printer.print(expression))