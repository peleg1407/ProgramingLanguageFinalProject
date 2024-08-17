from environment import Environment
from lexer import TokenType
from parser import Function, Return

class Interpreter:
    def __init__(self):
        self.global_env = Environment()

    def visit(self, node, env):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, env)

    def generic_visit(self, node, env):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_BinOp(self, node, env):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left, env) + self.visit(node.right, env)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left, env) - self.visit(node.right, env)
        elif node.op.type == TokenType.MULTIPLY:
            return self.visit(node.left, env) * self.visit(node.right, env)
        elif node.op.type == TokenType.DIVIDE:
            return self.visit(node.left, env) // self.visit(node.right, env)
        elif node.op.type == TokenType.MODULO:
            return self.visit(node.left, env) % self.visit(node.right, env)
        elif node.op.type == TokenType.AND:
            return self.visit(node.left, env) and self.visit(node.right, env)
        elif node.op.type == TokenType.OR:
            return self.visit(node.left, env) or self.visit(node.right, env)
        elif node.op.type == TokenType.EQUAL:
            return self.visit(node.left, env) == self.visit(node.right, env)
        elif node.op.type == TokenType.NOT_EQUAL:
            return self.visit(node.left, env) != self.visit(node.right, env)
        elif node.op.type == TokenType.GREATER:
            return self.visit(node.left, env) > self.visit(node.right, env)
        elif node.op.type == TokenType.LESS:
            return self.visit(node.left, env) < self.visit(node.right, env)
        elif node.op.type == TokenType.GREATER_EQUAL:
            return self.visit(node.left, env) >= self.visit(node.right, env)
        elif node.op.type == TokenType.LESS_EQUAL:
            return self.visit(node.left, env) <= self.visit(node.right, env)

    def visit_UnaryOp(self, node, env):
        if node.op.type == TokenType.PLUS:
            return +self.visit(node.expr, env)
        elif node.op.type == TokenType.MINUS:
            return -self.visit(node.expr, env)
        elif node.op.type == TokenType.NOT:
            return not self.visit(node.expr, env)

    def visit_Num(self, node, env):
        return node.value

    def visit_Bool(self, node, env):
        return node.value

    def visit_Var(self, node, env):
        return env.get(node.value)

    def visit_Function(self, node, env):
        func = Function(node.name, node.params, node.body, env)
        env.set(node.name, func)
        return func

    def visit_Lambda(self, node, env):
        return Function(None, node.params, node.body, env)

    def visit_Call(self, node, env):
        func = self.visit(node.func, env)
        if not isinstance(func, Function):
            raise Exception(f'{func} is not a function')
        if len(func.params) != len(node.args):
            raise Exception('Argument count mismatch')
        new_env = Environment(func.env)
        for param, arg in zip(func.params, node.args):
            new_env.set(param, self.visit(arg, env))
        result = self.visit(func.body, new_env)
        if isinstance(result, Return):
            return result.value
        return result

    def visit_If(self, node, env):
        condition = self.visit(node.condition, env)
        if condition:
            return self.visit(node.then_branch, env)
        elif node.else_branch:
            return self.visit(node.else_branch, env)
        return None

    def visit_Return(self, node, env):
        return Return(self.visit(node.value, env))

    def eval(self, node, env=None):
        if env is None:
            env = self.global_env
        return self.visit(node, env)
