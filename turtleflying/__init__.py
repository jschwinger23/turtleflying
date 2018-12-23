def monkey_patch(signal=True, sleep=True, socket=True):
    if signal:
        import signal
        from .signal import green_signal
        signal._o_signal, signal.signal = signal.signal, green_signal

    if sleep:
        import time
        from .sleep import green_sleep
        time._o_sleep, time.sleep = time.sleep, green_sleep

    if socket:
        import socket
        from .socket import get_socket
        socket._o_socket, socket.socket = socket.socket, get_socket
