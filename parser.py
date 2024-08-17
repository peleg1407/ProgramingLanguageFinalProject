from lexer import TokenType

class AST:
    pass

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Bool(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class If(AST):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class Function(AST):
    def __init__(self, name, params, body, env=None):
        self.name = name
        self.params = params
        self.body = body
        self.env = env

class Lambda(AST):
    def __init__(self, params, body):
        self.params = params
        self.body = body

class Call(AST):
    def __init__(self, func, args):
        self.func = func
        self.args = args

class Return(AST):
    def __init__(self, value):
        self.value = value

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.BOOLEAN:
            self.eat(TokenType.BOOLEAN)
            return Bool(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        elif token.type == TokenType.IDENTIFIER:
            var_token = token
            self.eat(TokenType.IDENTIFIER)
            if self.current_token.type == TokenType.LPAREN:
                self.eat(TokenType.LPAREN)
                args = []
                if self.current_token.type != TokenType.RPAREN:
                    args.append(self.expr())
                    while self.current_token.type == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                        args.append(self.expr())
                self.eat(TokenType.RPAREN)
                return Call(var_token, args)
            return Var(var_token)
        elif token.type == TokenType.LAMBDA:
            return self.lambda_expr()
        else:
            self.error()

    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
            elif token.type == TokenType.MODULO:
                self.eat(TokenType.MODULO)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def comparison(self):
        node = self.expr()
        if self.current_token.type in (TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.GREATER, TokenType.LESS, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL):
            token = self.current_token
            if token.type == TokenType.EQUAL:
                self.eat(TokenType.EQUAL)
            elif token.type == TokenType.NOT_EQUAL:
                self.eat(TokenType.NOT_EQUAL)
            elif token.type == TokenType.GREATER:
                self.eat(TokenType.GREATER)
            elif token.type == TokenType.LESS:
                self.eat(TokenType.LESS)
            elif token.type == TokenType.GREATER_EQUAL:
                self.eat(TokenType.GREATER_EQUAL)
            elif token.type == TokenType.LESS_EQUAL:
                self.eat(TokenType.LESS_EQUAL)
            node = BinOp(left=node, op=token, right=self.expr())
        return node

    def boolean_expr(self):
        node = self.comparison()
        while self.current_token.type in (TokenType.AND, TokenType.OR):
            token = self.current_token
            if token.type == TokenType.AND:
                self.eat(TokenType.AND)
            elif token.type == TokenType.OR:
                self.eat(TokenType.OR)
            node = BinOp(left=node, op=token, right=self.comparison())
        return node

    def block(self):
        self.eat(TokenType.LBRACE)
        statements = []
        while self.current_token.type != TokenType.RBRACE:
            statements.append(self.statement())
        self.eat(TokenType.RBRACE)
        if len(statements) == 1:
            return statements[0]
        return statements

    def statement(self):
        if self.current_token.type == TokenType.DEFUN:
            self.eat(TokenType.DEFUN)
            func_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.LPAREN)
            params = []
            if self.current_token.type == TokenType.IDENTIFIER:
                params.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    params.append(self.current_token.value)
                    self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.RPAREN)
            body = self.block()
            return Function(func_name, params, body)
        elif self.current_token.type == TokenType.IF:
            self.eat(TokenType.IF)
            condition = self.boolean_expr()
            then_branch = self.block()
            else_branch = None
            if self.current_token.type == TokenType.ELSE:
                self.eat(TokenType.ELSE)
                else_branch = self.block()
            return If(condition, then_branch, else_branch)
        elif self.current_token.type == TokenType.RETURN:
            self.eat(TokenType.RETURN)
            expr = self.expr()
            return Return(expr)
        else:
            return self.boolean_expr()

    def lambda_expr(self):
        self.eat(TokenType.LAMBDA)
        params = []
        if self.current_token.type == TokenType.IDENTIFIER:
            params.append(self.current_token.value)
            self.eat(TokenType.IDENTIFIER)
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                params.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ARROW)
        body = self.expr()
        return Lambda(params, body)

    def parse(self):
        return self.statement()
