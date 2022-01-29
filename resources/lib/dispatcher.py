from .common import params

class Dispatcher:
    functions = {}
    args = {}
    kwargs = {}
    def register(self, route: str, args = [], kwargs = []):
        def add(f):
            if route in self.functions:
                raise Exception(f'{route} route already exists!')

            self.functions[route] = f
            self.args[route] = args
            self.kwargs[route] = kwargs
            return f

        return add

    def run(self, route: str):
        if route not in self.functions:
            raise Exception('Route not valid')

        args = []
        kwargs = []
        # Add args
        if self.args[route]:
            for arg in self.args[route]:
                if arg not in params:
                    raise Exception('Param not found in URL!')

                args.append(params[arg])

        self.functions[route](*args)
