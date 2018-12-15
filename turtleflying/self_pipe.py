import os


class SelfPipe:
    _instances = {}

    @classmethod
    def get_or_create(cls, *, namespace='default'):
        created = False
        if namespace not in cls._instances:
            cls._instances[namespace] = cls(namespace)
            created = True
        return cls._instances[namespace], created

    def __init__(self, namespace):
        self.namespace = namespace
        self.pipe_pair = os.pipe2(os.O_NONBLOCK | os.O_CLOEXEC)

    @property
    def write_end(self):
        return self.pipe_pair[1]

    @property
    def read_end(self):
        return self.pipe_pair[0]
