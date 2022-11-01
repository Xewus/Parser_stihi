from typing import Callable

def need_implement_in_subclass(func: Callable):
    def wrap(*a, **kw):
        raise NotImplementedError(
            'Нужно реализовать метод `%s` в наследнике' % func.__name__
        )
    return wrap
