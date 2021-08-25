import argparse
import sys
from typing import List

from ast_printer import AstPrinter
from exceptions import LoxRuntimeError
from expr import Expr
from interpreter import Interpreter
from lox_parser import Parser
from scanner import Scanner
from tokens import Token

class Lox():
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False
        self.interpreter = Interpreter()

    def run_file(self, filename: str):
        with open(filename, 'r') as f:
            self.run(f.read())
        if self.had_error:
            sys.exit(65)
        if self.had_runtime_error:
            sys.exit(70)

    def run_prompt(self):
        print("Lox 0.x. Type quit() to exit.")
        line = input(">")
        while line != "quit()":
            self.run(line, repl=True)
            self.had_error = False
            line = input(">")

    def run(self, source: str, repl: bool = False):
        scanner = Scanner(source, self.error)
        tokens: List[Token] = scanner.scan_tokens()
        parser = Parser(tokens, self.report)
        statements = parser.parse()

        if self.had_error:
            return
        
        try:
            self.interpreter.interpret(statements, repl)
        except LoxRuntimeError as e:
            self.runtime_error(e)

    def error(self, line: int, msg: str):
        self.report(line, "", msg)

    def runtime_error(self, error: LoxRuntimeError):
        print(f"{error.message}\n[line {error.token.line}]", file=sys.stderr)
        self.had_runtime_error = True

    def report(self, line: int, where: str, msg: str):
        print(f"[line {line}] Error{where}: {msg}", file=sys.stderr)
        self.had_error = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Python implementation of Lox")
    parser.add_argument("--filename", help="Lox file to run")
    args = parser.parse_args()

    lox = Lox()
    if args.filename:
        lox.run_file(args.filename)
    else:
        lox.run_prompt()