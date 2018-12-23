import os

from typing import Optional
from functools import wraps
from greenlet import greenlet as Greenlet

from .helper import wait
from .utils import SelfPipe, Timeout


class Coroutine:

    @classmethod
    def current(cls) -> 'Coroutine':
        return cls(greenlet=Greenlet.getcurrent())

    def __init__(
        self,
        *,
        target: Optional[callable] = None,
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
        greenlet: Optional[Greenlet] = None,
    ):
        self._finish_event = Event()
        if greenlet:
            target = greenlet.run

        @wraps(target)
        def wrapper():
            target(*args, **kwargs)
            self._finish_event.set()

        self.greenlet = Greenlet(wrapper)

    def resume(self, *args, **kws):
        return self.greenlet.switch(*args, **kws)

    start = resume

    def is_alive(self) -> bool:
        return not self.greenlet.dead

    def join(self, timeout: Optional[int] = None):
        self._finish_event.wait()

    def kill(self):
        self.greenlet.throw()
        for fd in coroutine._fds:
            pass


class Event:

    def __init__(self):
        self._pipe = SelfPipe()

    def set(self):
        os.write(self._pipe.write_end, b'\0')

    def wait(self, timeout=None) -> bool:
        try:
            with Timeout(timeout):
                wait(on_readable=self._pipe.read_end)
        except TimeoutError:
            return False
        else:
            return True
