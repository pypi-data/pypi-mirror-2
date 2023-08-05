# Copyright (c) 2010 Jean-Paul Calderone.
# See LICENSE file for details.

try:
    from signalfd._signalfd import \
        sigprocmask, signalfd, \
        SIG_BLOCK, SIG_UNBLOCK, SIG_SETMASK, \
        SFD_CLOEXEC, SFD_NONBLOCK
except ImportError:
    from _signalfd import \
        sigprocmask, signalfd, \
        SIG_BLOCK, SIG_UNBLOCK, SIG_SETMASK, \
        SFD_CLOEXEC, SFD_NONBLOCK

__version__ = '0.1'
__version_info__ = (0, 1)

__all__ = [
    'sigprocmask', 'signalfd',

    'SIG_BLOCK', 'SIG_UNBLOCK', 'SIG_SETMASK',

    'SFD_CLOEXEC', 'SFD_NONBLOCK',

    '__version__', '__version_info__']
