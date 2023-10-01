class Dispatcher:
    def __init__(self):
        self.table = {}

    def register(self, name, func):
        self.table[name] = func

    def __call__(self, name, *args):
        if name in self.table:
            return self.table[name](*args)


def modify_list(items: list[int]) -> list[int]:
    my_dispatcher = Dispatcher()
    my_dispatcher.register("x", lambda x: x**2)
    return [my_dispatcher("x", item) for item in items]
