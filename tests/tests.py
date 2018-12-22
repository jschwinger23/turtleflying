import turtleflying
turtleflying.monkey_patch()

import time
import signal


def int_handler(_, __):
    print('sigint!')


signal.signal(signal.SIGINT, int_handler)

time.sleep(3)
print('resume')
