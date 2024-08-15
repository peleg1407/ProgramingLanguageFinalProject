import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def run_file(filename):
    if not filename.endswith('.lambda'):
        raise Exception('File must have a .lambda suffix')
    with open(filename, 'r') as file:
        source_code = file.read()
    lexer = Lexer(source_code)
    parser = Parser(lexer)
    ast = parser.parse()
    interpreter = Interpreter()
    result = interpreter.eval(ast)
    print(result)

def repl():
    print("Lambda Interpreter REPL. Type 'exit' to quit.")
    interpreter = Interpreter()
    env = interpreter.global_env
    while True:
        try:
            line = input('>>> ')
            if line.strip().lower() == 'exit':
                break
            lexer = Lexer(line)
            parser = Parser(lexer)
            ast = parser.parse()
            result = interpreter.eval(ast, env)
            print(result)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        repl()
