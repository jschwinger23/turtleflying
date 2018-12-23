import os
import timerfd

from .time import sleep
from .coroutine import Coroutine


def get_timerfd(seconds: int):
    fd = timerfd.create(timerfd.CLOCK_REALTIME, 0)
    timerfd.settime(fd, 0, seconds, 0)
    return fd


class SelfPipe:

    def __init__(self):
        self.pipe_pair = os.pipe2(os.O_NONBLOCK | os.O_CLOEXEC)

    @property
    def write_end(self):
        return self.pipe_pair[1]

    @property
    def read_end(self):
        return self.pipe_pair[0]


class Timeout:

    def __init__(self, timeout: int):
        self.timeout = timeout
        self._coroutine: Coroutine = None

    def __enter__(self):
        self._coroutine = Coroutine(target=self.raise_after_timeout)
        self._coroutine.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._coroutine.kill()
        return True

    def raise_after_timeout(self):
        sleep(self.timeout)
        raise TimeoutError
