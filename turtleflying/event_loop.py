import os
import signal
import timerfd
import greenlet
import selectors
from typing import Callable

from .self_pipe import SelfPipe


class EventLoop:
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._running = False
        self._greenlet: greenlet.greenlet = None
        self._selector = selectors.DefaultSelector()

        self._sig_handlers = {}
        self._sig_pending = set()  # ordering for CPython3.6+
        self._sig_wakeup_fd: int = None

    def is_running(self):
        return self._running

    def run_forever(self):
        self._running = True

        while self._running:
            for key, event in self._selector.select():
                key.data(key.fileobj, event)

    def stop(self):
        self._running = False

    def add_reader(self, fd, callback, *args):
        self._selector.register(
            fd,
            selectors.EVENT_READ,
            lambda _, __: callback(*args),
        )

    def call_later(self, delay: int, callback: Callable, *args):
        fd = timerfd.create(timerfd.CLOCK_REALTIME, 0)
        timerfd.settime(fd, 0, delay, 0)
        self.add_reader(fd, callback, *args)

    def add_signal_handler(self, signum: int, handler: Callable, *args):
        self._sig_handlers[signum] = lambda: handler(*args)

        self_pipe, created = SelfPipe.get_or_create(namespace='signal')
        if created:

            def handle_signals():
                for sig in self._sig_pending:
                    self._sig_handlers[sig]()
                self._sig_pending.clear()

            self._sig_wakeup_fd = self_pipe.write_end
            self.add_reader(self_pipe.read_end, handle_signals)

            def _handler(signum, frame):
                self._sig_pending.add(signum)
                os.write(self._sig_wakeup_fd, b'.')

            signal._o_signal(signum, _handler)

    def switch(self):
        if not self.is_running():
            self.greenlet = greenlet.greenlet(self.run_forever)
        self.greenlet.switch()
