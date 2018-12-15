import greenlet


def green_sleep(secs):
    from .event_loop import EventLoop
    event_loop = EventLoop.instance()
    crt_greenlet = greenlet.getcurrent()

    def switch_back():
        crt_greenlet.switch()

    event_loop.call_later(secs, switch_back)
    event_loop.switch()
