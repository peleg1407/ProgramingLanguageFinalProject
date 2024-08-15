import unittest
from lexer import Lexer, TokenType

class TestLexer(unittest.TestCase):
    def test_integer(self):
        lexer = Lexer("123")
        token = lexer.get_next_token()
        self.assertEqual(token.type, TokenType.INTEGER)
        self.assertEqual(token.value, 123)

    def test_boolean(self):
        lexer = Lexer("true")
        token = lexer.get_next_token()
        self.assertEqual(token.type, TokenType.BOOLEAN)
        self.assertEqual(token.value, True)

    def test_identifier(self):
        lexer = Lexer("variable")
        token = lexer.get_next_token()
        self.assertEqual(token.type, TokenType.IDENTIFIER)
        self.assertEqual(token.value, "variable")

if __name__ == '__main__':
    unittest.main()
