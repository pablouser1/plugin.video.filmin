from .common import params

class Dispatcher:
    functions = {}
    args = {}
    def register(self, route: str, args = []):
        def add(f):
            if route in self.functions:
                raise Exception(f'{route} route already exists!')

            self.functions[route] = f
            self.args[route] = args
            return f

        return add

    def run(self, route: str):
        if route not in self.functions:
            raise Exception('Route not valid')

        args = []
        # Add args
        if self.args[route]:
            for arg in self.args[route]:
                if arg not in params:
                    raise Exception('Param not found in URL!')

                args.append(params[arg])

        self.functions[route](*args)
