from .utils import get_timerfd
from .event_loop import EventLoop

from .coroutine import Coroutine


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

    fd_manager.add(on_readable or on_writable)

    coroutine_yield()


def coroutine_yield():
    global EVENT_LOOP_COROUTINE
    if not EVENT_LOOP_COROUTINE:
        event_loop = EventLoop.get_event_loop()
        EVENT_LOOP_COROUTINE = Coroutine(event_loop.run_forever)
    EVENT_LOOP_COROUTINE.resume()


def coroutine_resume():
    coroutine = Coroutine.current()
    def _resume(fd, event):
        event_loop.unregister(fd)
        coroutine.resume()
    return _resume
