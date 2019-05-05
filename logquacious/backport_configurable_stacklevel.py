"""
Backport of configurable stacklevel for logging added in Python 3.8.

See https://github.com/python/cpython/pull/7424
"""
import io
import logging
import os
import sys
import traceback
from contextlib import contextmanager


__all__ = ['PatchedLoggerMixin', 'patch_logger']


class PatchedLoggerMixin(object):
    """Mixin adding `temp_monkey_patched_logger` that allows stacklevel kwarg.

    Classes that include this mixin have a `temp_monkey_patched_logger`
    context manager that allows the use of the `stacklevel` keyword argument
    from Python 3.8.

    Classes using this mixin must have a `logging.Logger` instance as an
    attribute of the class. By default, this is assumed to be named `logger`,
    but you can override the `logger_attribute` class attribute with the
    name of a different attribute.
    """

    #: Name of logger instance on the class inheriting this mixin.
    logger_attribute = 'logger'

    def __init__(self, *args, **kwargs):
        super(PatchedLoggerMixin, self).__init__(*args, **kwargs)
        self._patched_logger_class = None

    def _get_logger(self):
        if not hasattr(self, self.logger_attribute):
            msg = (
                "Subclass of PatchedLoggerMixin must define `{}` attribute "
                "or override `logger_attribute`".format(self.logger_attribute)
            )
            raise AttributeError(msg)
        return getattr(self, self.logger_attribute)

    @contextmanager
    def temp_monkey_patched_logger(self):
        """Temporarily monkey patch logger to allow overriding log records.

        The monkey patching is reset so that the behavior change is limited
        to the scope of this logger.
        """
        logger = self._get_logger()
        original_logger_class = logger.__class__

        # Cache patched logger class if not already defined.
        if self._patched_logger_class is None:
            self._patched_logger_class = patch_logger(logger.__class__)

        logger.__class__ = self._patched_logger_class
        try:
            yield
        finally:
            logger.__class__ = original_logger_class


def patch_logger(logger_class):
    """Return logger class patched with stacklevel keyword argument."""
    if sys.version_info.major >= 3 and sys.version_info.minor >= 8:
        return logger_class
    return type('ConfigurableStacklevelLogger',
                (ConfigurableStacklevelLoggerMixin, logger_class), {})


class ConfigurableStacklevelLoggerMixin(object):
    """Mixin for adding `stacklevel` keyword argument for logging methods.

    This mixin can be used to monkey patch `logging.Logger` to include the
    `stacklevel` keyword argument that will be available in Python 3.8.

    See https://github.com/python/cpython/pull/7424
    """

    def findCaller(self, stack_info=False, stacklevel=1):  # pragma: no cover
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = logging.currentframe()
        # On some versions of IronPython, currentframe() returns None if
        # IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        orig_f = f
        while f and stacklevel > 1:
            f = f.f_back
            stacklevel -= 1
        if not f:
            f = orig_f
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == logging._srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv

    def _log(self, level, msg, args, exc_info=None, extra=None,
             stack_info=False, stacklevel=1):  # pragma: no cover
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        sinfo = None
        if logging._srcfile:
            # IronPython doesn't track Python frames, so findCaller raises an
            # exception on some versions of IronPython. We trap it here so that
            # IronPython can use logging.
            try:
                fn, lno, func, sinfo = self.findCaller(stack_info, stacklevel)
            except ValueError:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()

        if sys.version_info.major >= 3:
            record = self.makeRecord(self.name, level, fn, lno, msg, args,
                                     exc_info, func, extra, sinfo)
        else:
            record = self.makeRecord(self.name, level, fn, lno, msg, args,
                                     exc_info, func, extra)
        self.handle(record)
