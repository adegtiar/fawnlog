import time

NANOS_PER_SECOND = 1.0 * 1000 * 1000


def nanotime():
    return int(time.time() * NANOS_PER_SECOND)

def nanos_to_sec(nanos):
    return nanos / NANOS_PER_SECOND
