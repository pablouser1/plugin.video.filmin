""" Dispacher for router """

from .common import _PARAMS
from .constants import Routes


class Dispatcher:
    """
    Handle routing
    """

    functions = {}
    args = {}

    def register(self, route: Routes, args: list = None):
        """
        Add route to system
        """

        if args is None:
            args = []

        val = route.value

        def add(func):
            if val in self.functions:
                raise ValueError(f"{route} route already exists!")

            self.functions[val] = func
            self.args[val] = args
            return func

        return add

    def run(self, route: str):
        """
        Run current route, taken from _PARMS from .config
        """

        if route not in self.functions:
            raise ValueError("Route not valid")

        args = []
        # Add args
        if self.args[route]:
            for arg in self.args[route]:
                if arg not in _PARAMS:
                    raise ValueError("Param not found in URL!")

                args.append(_PARAMS[arg])

        self.functions[route](*args)
