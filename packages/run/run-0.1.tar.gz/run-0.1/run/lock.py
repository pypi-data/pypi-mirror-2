import fcntl
import sys

from run.base import AlreadyLocked

def lock(fd):
    if not hasattr(fd, 'fileno'):
        fd = file(fd)
    if not fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB):
        raise AlreadyLocked(fd)

