from typing import Callable
from greenlet import greenlet as Greenlet

from .utils import multipledispatch


class Coroutine:

    @classmethod
    def current(cls) -> 'Coroutine':
        return cls(Greenlet.getcurrent())

    @multipledispatch
    def __init__(self, greenlet: Greenlet):
        self.greenlet = greenlet

    @multipledispatch
    def __init__(self, func: Callable):
        self.greenlet = Greenlet(func)

    def resume(self):
        return self.greenlet.switch()
