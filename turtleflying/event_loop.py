import asyncio
import selectors
from typing import Callable

FD = int
EVENT = int


class EventLoop(asyncio.AbstractEventLoop):
    _instance = None

    @classmethod
    def get_event_loop(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._running = False
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

    def add_reader(self, fd: FD, callback: Callable[[FD, EVENT]]):
        self._selector.register(
            fd,
            selectors.EVENT_READ,
            callback,
        )

    def add_writer(self, fd: FD, callback: Callable[[FD, EVENT]]):
        self._selector.register(
            fd,
            selectors.EVENT_WRITE,
            callback,
        )

    def remove_reader(self, fd: FD) -> bool:
        try:
            self._selector.get_key(fd)
        except KeyError:
            return False
        else:
            self._selector.unregister(fd)
            return True

    remove_writer = remove_reader
