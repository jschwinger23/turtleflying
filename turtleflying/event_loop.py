import asyncio
import selectors
from typing import Callable

from .coroutine import Coroutine


class EventLoop(asyncio.AbstractEventLoop):
    _instance = None

    @classmethod
    def get_event_loop(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._running = False
        self._coroutine: Coroutine = None
        self._selector = selectors.DefaultSelector()

    def is_running(self):
        return self._running

    def run_forever(self):
        self._running = True

        while self._running:
            for key, event in self._selector.select():
                key.data(key.fileobj, event)

    def stop(self):
        self._running = False

    def add_reader(self, fd: int, callback: Callable, *args):
        self._selector.register(
            fd,
            selectors.EVENT_READ,
            lambda *_: callback(*args),
        )

    def add_writer(self, fd: int, callback: Callable, *args):
        self._selector.register(
            fd,
            selectors.EVENT_WRITE,
            lambda *_: callback(*args),
        )

    def get_coroutine(self) -> Coroutine:
        if not self.is_running():
            self._coroutine = Coroutine(self.run_forever)

        return self._coroutine


def coroutine_yield():
    event_loop = EventLoop.get_event_loop()
    coroutine = event_loop.get_coroutine()
    coroutine.resume()


def coroutine_resume():
    coroutine = Coroutine.current()
    return coroutine.resume
