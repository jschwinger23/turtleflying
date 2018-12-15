def green_signal(signalnum, handler):
    from .event_loop import EventLoop
    event_loop = EventLoop.instance()
    event_loop.add_signal_handler(signalnum, handler)
