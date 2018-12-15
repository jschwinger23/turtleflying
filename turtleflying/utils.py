import signal
import contextlib
from typing import Sequence


@contextlib.contextmanager
def block_signals(signals: Sequence[int]):
    signals = signals.copy()
    signal.pthread_sigmask(signal.SIG_BLOCK, signals)
    yield
    signal.pthread_sigmask(signal.SIG_UNBLOCK, signals)
