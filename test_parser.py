import unittest
from lexer import Lexer
from parser import Parser, Num, BinOp, Lambda, Var


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

    def test_lambda_expression(self):
        lexer = Lexer("lambda x, y -> x + y")
        parser = Parser(lexer)
        ast = parser.parse()
        self.assertIsInstance(ast, Lambda)
        self.assertEqual(ast.params, ['x', 'y'])
        self.assertIsInstance(ast.body, BinOp)
        self.assertIsInstance(ast.body.left, Var)
        self.assertEqual(ast.body.left.value, 'x')
        self.assertIsInstance(ast.body.right, Var)
        self.assertEqual(ast.body.right.value, 'y')

if __name__ == '__main__':
    unittest.main()