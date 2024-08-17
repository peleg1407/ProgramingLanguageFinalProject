from enum import Enum, auto

class TokenType(Enum):
    INTEGER = auto()
    BOOLEAN = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    LPAREN = auto()
    RPAREN = auto()
    IDENTIFIER = auto()
    LAMBDA = auto()
    DEFUN = auto()
    COMMA = auto()
    LBRACE = auto()
    RBRACE = auto()
    IF = auto()
    ELSE = auto()
    EOF = auto()
    ARROW = auto()
    RETURN = auto()

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.current_char = self.source_code[self.position]

    def advance(self):
        """Move the cursor one character forward."""
        self.position += 1
        if self.position < len(self.source_code):
            self.current_char = self.source_code[self.position]
        else:
            self.current_char = None

    def skip_whitespace(self):
        """Skip any whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        """Skip comments that start with a '#' character."""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        self.advance()

    def integer(self):
        """Extract an integer from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self):
        """Extract an identifier or a keyword like 'defun', 'lambda', or 'return'."""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        if result == 'true' or result == 'false':
            return Token(TokenType.BOOLEAN, result == 'true')
        elif result == 'defun':
            return Token(TokenType.DEFUN, result)
        elif result == 'lambda':
            return Token(TokenType.LAMBDA, result)
        elif result == 'return':
            return Token(TokenType.RETURN, result)
        else:
            return Token(TokenType.IDENTIFIER, result)

    def get_next_token(self):
        """Lexical analysis: Convert input into a stream of tokens."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char == '#':
                self.skip_comment()
                continue
            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())
            if self.current_char.isalpha():
                return self.identifier()
            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS)
            if self.current_char == '-':
                self.advance()
                if self.current_char == '>':
                    self.advance()
                    return Token(TokenType.ARROW)
                return Token(TokenType.MINUS)
            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY)
            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE)
            if self.current_char == '%':
                self.advance()
                return Token(TokenType.MODULO)
            if self.current_char == '&' and self.peek() == '&':
                self.advance()
                self.advance()
                return Token(TokenType.AND)
            if self.current_char == '|' and self.peek() == '|':
                self.advance()
                self.advance()
                return Token(TokenType.OR)
            if self.current_char == '!':
                self.advance()
                return Token(TokenType.NOT)
            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.EQUAL)
            if self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.NOT_EQUAL)
            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.GREATER_EQUAL)
                return Token(TokenType.GREATER)
            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.LESS_EQUAL)
                return Token(TokenType.LESS)
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN)
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN)
            if self.current_char == '{':
                self.advance()
                return Token(TokenType.LBRACE)
            if self.current_char == '}':
                self.advance()
                return Token(TokenType.RBRACE)
            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA)

            raise Exception(f'Invalid character: {self.current_char}')

        return Token(TokenType.EOF)

    def peek(self):
        """Peek at the next character without advancing the cursor."""
        peek_pos = self.position + 1
        if peek_pos < len(self.source_code):
            return self.source_code[peek_pos]
        else:
            return None
