import enum


class TokenType(enum.Enum):
  # Single-character tokens.
  LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE, COMMA, DOT, MINUS, PLUS, SEMICOLON, SLASH, STAR, = range(11)

  # One or two character tokens.
  BANG, BANG_EQUAL, EQUAL, EQUAL_EQUAL, GREATER, GREATER_EQUAL, LESS, LESS_EQUAL = range(12, 20)
  # Literals.
  IDENTIFIER, STRING, NUMBER = range(20, 23)

  # Keywords.
  AND, CLASS, ELSE, FALSE, FUN, FOR, IF, NIL, OR, PRINT, RETURN, SUPER, THIS, TRUE, VAR, WHILE = range(23, 39)

  EOF = 39