from .queue import Queue
from .sleep import sleep
from .coroutine import Coroutine


class Pool:

    def __init__(self, maxsize: int = 1000):
        self.maxsize = maxsize
        self._pool = []
        self._repopulate_pool()
        self._inqueue = Queue(maxsize)
        self._maintainer = Coroutine(target=self._maintain_pool)
        self._maintainer.start()

    def spawn(self, func, *args, **kws):
        self._inqueue.put((func, args, kws))

    def _repopulate_pool(self):
        for _ in range(self.maxsize - len(self._pool)):
            coroutine = Coroutine(target=self.worker, args=(self._inqueue,))
            self._pool.append(coroutine)
            coroutine.start()

    def _maintain_pool(self):
        while True:
            if self._join_exited_workers():
                self._repopulate_pool()
            sleep(1)

    def _join_exited_workers(self):
        cleaned = False
        for idx, coroutine in enumerate(self._pool):
            if not coroutine.is_alive():
                coroutine.join()
                del self._pool[idx]
                cleaned = True
        return cleaned

    def _consume(self, queue):
        while True:
            func, args, kws = queue.get()
            func(*args, **kws)
