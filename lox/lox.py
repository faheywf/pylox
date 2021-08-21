import argparse
import sys
from typing import List

from scanner import Scanner


class Lox():
    def __init__(self):
        self.had_error = False

    def run_file(self, filename: str):
        with open(filename, 'r') as f:
            self.run(f.read())
        if self.had_error:
            sys.exit(65)

    def run_prompt(self):
        print("Lox 0.x. Type quit() to exit.")
        line = input(">")
        while line != "quit()":
            self.run(line)
            self.had_error = False
            line = input(">")

    def run(self, source: str):
        scanner = Scanner(source, self.error)
        tokens: List[Token] = scanner.scan_tokens()

        for token in tokens:
            print(token)

    def error(self, line: int, msg: str):
        self.report(line, "", msg)

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