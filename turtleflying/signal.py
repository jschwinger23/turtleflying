import os
import signal
from typing import Dict, Callable

from .utils import SelfPipe
from .event_loop import EventLoop


def green_signal(signum, handler):
    signal_hub = SignalHub.get()
    signal_hub.register(signum, handler)


class SignalHub:
    _instance = None

    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.handler: Dict[int, Callable] = {}
        self.pipe = SelfPipe()
        signal.set_wakeup_fd(self.pipe.write_end, warn_on_full_buffer=True)
        event_loop = EventLoop.get_event_loop()
        event_loop.add_reader(self.pipe.read_end, self.handle)

    def register(self, signum: int, handler: Callable):
        signal._o_signal(signum, lambda *args: None)
        self.handler[signum.value] = handler

    def handle(self):
        while True:
            try:
                signum = ord(os.read(self.pipe.read_end, 1))
            except BlockingIOError:
                break
            else:
                self.handler[signum](signum, None)
