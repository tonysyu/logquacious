import logging
from contextlib import contextmanager

from . import utils
from .log_context import LogContext


class LogManager:
    """Logging manager for use as a logger, decorator, or contextmanager.

    >>> log = LogManager(__name__)
    >>> log.info('Normal logging statement')

        [INFO] Normal logging statement

    >>> @log.context.info
    ... def logged_function():
    ...     log.info('Inside logged_function')

        [DEBUG] Start logged_function
        [INFO] Inside logged_function
        [DEBUG] Finish logged_function

    >>> with log.context.info("context manager"):
    ...     log.info("Inside context manager")

        [DEBUG] Start context manager
        [INFO] Inside context manger
        [DEBUG] Finish context manager
    """

    def __init__(self, name=None, context_templates=None):
        self.logger = utils.get_logger(name)
        self.context = LogContext(self.logger, context_templates)

    def log(self, level, msg, *args, **kwargs):
        """Log 'msg % args' with integer severity 'level'.

        This is a thin wrapper around `logging.Logger.log`.
        """
        return self.logger.log(level, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """Log 'msg % args' with integer severity `logging.DEBUG`.

        This is a thin wrapper around `logging.Logger.debug`.
        """
        return self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """Log 'msg % args' with integer severity `logging.INFO`.

        This is a thin wrapper around `logging.Logger.info`.
        """
        return self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """Log 'msg % args' with integer severity `logging.WARNING`.

        This is a thin wrapper around `logging.Logger.warning`.
        """
        return self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """Log 'msg % args' with integer severity `logging.ERROR`.

        This is a thin wrapper around `logging.Logger.error`.
        """
        return self.logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """Log 'msg % args' with integer severity `logging.ERROR` w/ exception.

        This is a thin wrapper around `logging.Logger.exception`.
        """
        return self.logger.exception(msg, *args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        """Log 'msg % args' with integer severity `logging.CRITICAL`.

        This is a thin wrapper around `logging.Logger.fatal`.
        """
        return self.logger.fatal(msg, *args, **kwargs)

    @contextmanager
    def and_suppress(self, allowed_exceptions,
                     msg="Suppressed error and logging",
                     level=logging.ERROR, exc_info=True):
        """Context manager that logs and suppreses given error.

        Arguments:
            allowed_exceptions: Exception(s) to log and suppress.
            msg: Message logged for exceptions.
            level: Logging level for logging exceptions.
            exc_info: If True, include exception info.
        """
        try:
            yield
        except allowed_exceptions:
            self.log(level, msg, exc_info=exc_info)

    @contextmanager
    def and_reraise(self, allowed_exceptions,
                    msg="Logging error and reraising",
                    level=logging.ERROR, exc_info=True):
        """Context manager that logs and reraises given error.

        Arguments:
            allowed_exceptions: Exception(s) to log before reraising.
            msg: Message logged for exceptions.
            level: Logging level for logging exceptions.
            exc_info: If True, include exception info.
        """
        try:
            yield
        except allowed_exceptions:
            self.log(level, msg, exc_info=exc_info)
            raise
