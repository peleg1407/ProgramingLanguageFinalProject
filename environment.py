class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise Exception(f'Undefined variable: {name}')

    def set(self, name, value):
        self.variables[name] = value
