import unittest
from lexer import Lexer
from parser import Parser, Num, BinOp


class TestParser(unittest.TestCase):
    def test_simple_expression(self):
        lexer = Lexer("3 + 4")
        parser = Parser(lexer)
        ast = parser.parse()
        self.assertIsInstance(ast, BinOp)
        self.assertIsInstance(ast.left, Num)
        self.assertEqual(ast.left.value, 3)
        self.assertIsInstance(ast.right, Num)
        self.assertEqual(ast.right.value, 4)

if __name__ == '__main__':
    unittest.main()
