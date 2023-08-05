# Copyright (c) 2010 Jean-Paul Calderone.
# See LICENSE file for details.

import sys

if sys.version_info < (3, 0):
    import unittest2 as unittest
    INTEGER_TYPES = (int, long)
else:
    import unittest
    INTEGER_TYPES = (int,)

import sys, os, errno, fcntl, signal, signalfd

class SomeException(Exception):
    """
    A unique exception class to be raised by a signal handler to verify that the
    signal handler was invoked.
    """


def raiser(*args):
    """
    A signal handler which raises SomeException.
    """
    raise SomeException()



class SigprocmaskTests(unittest.TestCase):
    """
    Tests for sigprocmask.
    """
    def _handle_sigusr1(self):
        old_handler = signal.signal(signal.SIGUSR1, raiser)
        self.addCleanup(signal.signal, signal.SIGUSR1, old_handler)

        # This depends on sigprocmask working a bit.  If it doesn't, then
        # this won't succeed in keeping the signal mask state sane.  But
        # there's nothing else we can do in that case.  This is necessary at
        # all because some environments start off with certain signals
        # masked for obscure reasons.  The intent is to provide the tests
        # with a consistent, predictable starting state and then restore the
        # environment's expectations after the test.
        old_mask = signalfd.sigprocmask(signalfd.SIG_SETMASK, [])
        self.addCleanup(signalfd.sigprocmask, signalfd.SIG_SETMASK, old_mask)


    def test_signature(self):
        """
        When invoked with other than two arguments, sigprocmask raises
        TypeError.
        """
        self.assertRaises(TypeError, signalfd.sigprocmask)
        self.assertRaises(TypeError, signalfd.sigprocmask, 1)
        self.assertRaises(TypeError, signalfd.sigprocmask, 1, 2, 3)


    def test_invalid_how(self):
        """
        If a value other than SIG_BLOCK, SIG_UNBLOCK, or SIG_SETMASK is passed
        for the how argument to sigprocmask, ValueError is raised.
        """
        message = "value specified for how (1700) invalid"
        try:
            signalfd.sigprocmask(1700, [])
        except ValueError:
            type, value, traceback = sys.exc_info()
            self.assertEquals(str(value), message)


    def test_invalid_signal_iterable(self):
        """
        If iterating over the value passed for the signals parameter to
        sigprocmask raises an exception, sigprocmask raises that exception.
        """
        class BrokenIter(object):
            def __iter__(self):
                raise RuntimeError("my __iter__ is broken")
        try:
            signalfd.sigprocmask(signalfd.SIG_BLOCK, BrokenIter())
        except RuntimeError:
            type, value, traceback = sys.exc_info()
            self.assertEquals(str(value), "my __iter__ is broken")


    def test_invalid_signal(self):
        """
        If an object in the iterable passed for the signals parameter to
        sigprocmask isn't an integer, TypeError is raised.
        """
        try:
            signalfd.sigprocmask(signalfd.SIG_BLOCK, [object()])
        except TypeError:
            type, value, traceback = sys.exc_info()
            self.assertEquals(str(value), "an integer is required")
        else:
            self.fail(
                "Expected non-integer signal to be rejected.")


    def test_return_previous_mask(self):
        """
        sigprocmask returns a list of the signals previously masked.
        """
        previous = signalfd.sigprocmask(signalfd.SIG_BLOCK, [1, 3, 5])
        result = signalfd.sigprocmask(signalfd.SIG_BLOCK, previous)
        self.assertEquals(result, [1, 3, 5])


    def test_block(self):
        """
        When invoked with SIG_BLOCK, sigprocmask blocks the signals in the
        sigmask list.
        """
        self._handle_sigusr1()
        previous = signalfd.sigprocmask(signalfd.SIG_BLOCK, [signal.SIGUSR1])
        os.kill(os.getpid(), signal.SIGUSR1)
        try:
            # Expect to receive SIGUSR1 after unblocking it.
            signalfd.sigprocmask(signalfd.SIG_SETMASK, previous)
        except SomeException:
            pass
        else:
            self.fail(
                "Expected exception to be raised after unblocking SIGUSR1")


    def test_unblock(self):
        """
        When invoked with SIG_UNBLOCK, sigprocmask unblocks the signals in the
        sigmask list.
        """
        self._handle_sigusr1()
        previous = signalfd.sigprocmask(signalfd.SIG_BLOCK, [signal.SIGUSR1])
        self.addCleanup(signalfd.sigprocmask, signalfd.SIG_SETMASK, previous)
        signalfd.sigprocmask(signalfd.SIG_UNBLOCK, [signal.SIGUSR1])

        try:
            os.kill(os.getpid(), signal.SIGUSR1)
        except SomeException:
            pass
        else:
            self.fail(
                "Expected SIGUSR1 to trigger handler raising SomeException")



class SignalfdTests(unittest.TestCase):
    """
    Tests for signalfd.signalfd.
    """
    def signalfd(self, *a, **kw):
        try:
            return signalfd.signalfd(*a, **kw)
        except OSError:
            type, value, traceback = sys.exc_info()
            if value.errno == errno.ENOSYS:
                raise unittest.Skip(
                    "signalfd() not implemented on this platform")


    def test_signature(self):
        """
        When invoked with fewer than two arguments or more than three, signalfd
        raises TypeError.
        """
        self.assertRaises(TypeError, self.signalfd)
        self.assertRaises(TypeError, self.signalfd, 1)
        self.assertRaises(TypeError, self.signalfd, 1, 2, 3, 4)


    def test_create_signalfd(self):
        """
        When invoked with a file descriptor of -1, signalfd allocates a new file
        descriptor for signal information delivery and returns it.
        """
        fd = self.signalfd(-1, [])
        self.assertIsInstance(fd, INTEGER_TYPES)
        os.close(fd)


    def test_non_iterable_signals(self):
        """
        If an object which is not iterable is passed for the sigmask list
        argument to signalfd, the exception raised by trying to iterate over
        that object is raised.
        """
        self.assertRaises(TypeError, self.signalfd, -1, object())


    def test_non_integer_signals(self):
        """
        If any non-integer values are included in the sigmask list argument to
        signalfd, the exception raised by the attempt to convert them to an
        integer is raised.
        """
        self.assertRaises(TypeError, self.signalfd, -1, [object()])


    def test_out_of_range_signal(self):
        """
        If a signal number that is out of the valid range is included in the
        sigmask list argument to signalfd, ValueError is raised.
        """
        message = "signal number -2 out of range"
        try:
            self.signalfd(-1, [-2])
        except ValueError:
            type, value, traceback = sys.exc_info()
            self.assertEquals(str(value), message)
        else:
            self.fail("Expected negative signal number to trigger ValueError")


    def test_handle_signals(self):
        """
        After signalfd is called, if a signal is received which was in the
        sigmask list passed to that call, information about the signal can be
        read from the fd returned by that call.
        """
        fd = self.signalfd(-1, [signal.SIGUSR2])
        self.addCleanup(os.close, fd)
        previous = signalfd.sigprocmask(signalfd.SIG_BLOCK, [signal.SIGUSR2])
        self.addCleanup(signalfd.sigprocmask, signalfd.SIG_SETMASK, previous)
        os.kill(os.getpid(), signal.SIGUSR2)
        bytes = os.read(fd, 128)
        self.assertTrue(bytes)


    def test_close_on_exec(self):
        """
        If the bit mask passed as the 3rd argument to signalfd includes
        SFD_CLOEXEC, the returned file descriptor has FD_CLOEXEC set on it.
        """
        fd = self.signalfd(-1, [], signalfd.SFD_CLOEXEC)
        self.addCleanup(os.close, fd)
        flags = fcntl.fcntl(fd, fcntl.F_GETFD)
        self.assertTrue(flags & fcntl.FD_CLOEXEC)


    def test_nonblocking(self):
        """
        If the bit mask passed as the 3rd argument to signalfd includes
        SFD_NOBLOCK, the file description referenced by the returned file
        descriptor has O_NONBLOCK set on it.
        """
        fd = self.signalfd(-1, [], signalfd.SFD_NONBLOCK)
        self.addCleanup(os.close, fd)
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        self.assertTrue(flags & os.O_NONBLOCK)


    def test_default_flags(self):
        """
        If an empty bit mask is passed as the 3rd argument to signalfd, neither
        FD_CLOEXEC nor O_NONBLOCK is set on the resulting file
        descriptor/description.
        """
        fd = self.signalfd(-1, [])
        self.addCleanup(os.close, fd)
        flags = fcntl.fcntl(fd, fcntl.F_GETFD)
        self.assertFalse(flags & fcntl.FD_CLOEXEC)
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        self.assertFalse(flags & os.O_NONBLOCK)


if __name__ == '__main__':
    unittest.main()
