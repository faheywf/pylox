from typing import Any, Callable, Dict, List, Optional, Tuple

from tokens import Token
from token_type import TokenType


class Scanner():
    def __init__(self, source: str, error: Callable[[int, str], None]):
        self.error = error
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

        self.source = source

        self.keywords: Dict[str, TokenType] = {
            "and": TokenType.AND,
            "break": TokenType.BREAK,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE
        }

    def scan_tokens(self):
        while self.current < len(self.source):
            self.start = self.current
            self.scan_token()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()

        if c == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c =="!":
            if self.match("="):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)
        elif c =="=":
            if self.match("="):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)
        elif c =="<":
            if self.match("="):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif c ==">":
            if self.match("="):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif c =="/":
            if self.match("/"):
                # a comment goes until the end of the line
                while self.peek() != "\n" and not self.is_at_end():
                    self.current += 1
            else:
                self.add_token(TokenType.SLASH)
        elif c in [" ", "\r", "\t"]:
            pass # ignore whitespace
        elif c == "\n":
            self.line += 1
        elif c == '"':
            self.string()
        elif c.isdigit():
            self.number()
        elif c.isalpha() or c == "_":
            self.identifier()
        else:
            self.error(self.line, "Unexpected character.")

    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    def add_token(self, token_type: TokenType, literal: Optional[Any] = None):
        token = Token(token_type, self.source[self.start:self.current], literal, self.line)
        self.tokens.append(token)

    def is_at_end(self) -> bool:
        return self.current > len(self.source)

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] == expected:
            self.current +=1
            return True
        return False

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 > len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        
        if self.is_at_end():
            self.error(self.line, "Unterminated string.")
            return

        self.advance() # consume closing "

        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.peek().isdigit():
            self.advance()
        
        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()

        while self.peek().isdigit():
            self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)