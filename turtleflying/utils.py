import os
import inspect
import timerfd
from typing import Callable
from functools import partial
from collections import defaultdict


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


def multipledispatch(func):
    dispatcher.register(func)
    return dispatcher
    return partial(dispatcher.dispatch, func.__name__)


class Dispatcher:

    def __init__(self):
        self.router = defaultdict(dict)

    def register(self, func: Callable):
        func_name = func.__name__
        members = inspect.getmembers(func)
        annotations = next(
            value for name, value in members if name == '__annotations__'
        )
        param_types = tuple(annotations.values())
        self.router[func_name][param_types] = func

    def dispatch(self, func_name, *args):
        for param_types, func in self.router[func_name].items():
            for arg, param_t in zip(args, param_types):
                if not isinstance(arg, param_t):
                    break
            else:
                return func
        raise ValueError('unsupported arguments')

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return lambda *args: self.dispatch(self.name, *args)(instance, *args)


dispatcher = Dispatcher()
