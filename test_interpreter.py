import unittest
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
    def test_simple_addition(self):
        source_code = "3 + 4"
        lexer = Lexer(source_code)
        parser = Parser(lexer)
        ast = parser.parse()
        interpreter = Interpreter()
        result = interpreter.eval(ast)
        self.assertEqual(result, 7)

    def test_factorial(self):
        source_code = """
        defun factorial(n) {
          if (n == 0) {
            return 1;
          } else {
            return n * factorial(n - 1);
          }
        }
        factorial(5)
        """
        lexer = Lexer(source_code)
        parser = Parser(lexer)
        ast = parser.parse()
        interpreter = Interpreter()
        result = interpreter.eval(ast)
        self.assertEqual(result, 120)

if __name__ == '__main__':
    unittest.main()
