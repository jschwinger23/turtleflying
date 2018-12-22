from .utils import get_timerfd
from .event_loop import EventLoop
from .event_loop import coroutine_yield, coroutine_resume


def wait(
    *,
    seconds: int = None,
    on_readable: int = None,
    on_writable: int = None,
):
    if seconds:
        on_readable = get_timerfd(seconds)

    event_loop = EventLoop.get_event_loop()
    if on_readable:
        event_loop.add_reader(on_readable, coroutine_resume())
    elif on_writable:
        event_loop.add_writer(on_writable, coroutine_resume())
    else:
        raise ValueError('nothing to wait')

    coroutine_yield()
