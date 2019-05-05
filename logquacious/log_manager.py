import logging

from . import utils
from .log_context import LogContext
from .backport_configurable_stacklevel import PatchedLoggerMixin


class LogManager(PatchedLoggerMixin):
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
        super(LogManager, self).__init__()

        self.logger = utils.get_logger(name)
        self.context = LogContext(self.logger, context_templates)

        # Alias `logging.Logger` methods:
        self.log = self.logger.log
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.exception = self.logger.exception
        self.fatal = self.logger.fatal

    def and_suppress(self, allowed_exceptions,
                     msg="Suppressed error and logging",
                     level=logging.ERROR, exc_info=True, stacklevel=3):
        """Context manager that logs and suppresses given error.

        Arguments:
            allowed_exceptions: Exception(s) to log and suppress.
            msg: Message logged for exceptions.
            level: Logging level for logging exceptions.
            exc_info: If True, include exception info.
            stacklevel: Stacklevel of logging statement. Defaults to level 3
                since this method (level=2) defers functionality to a helper
                utility (level=1), but logging should use the context where
                this is called (level=3).
        """
        def on_exception():
            with self.temp_monkey_patched_logger():
                self.log(level, msg, exc_info=exc_info, stacklevel=stacklevel)
            return True  # Return True suppresses error in __exit__

        return utils.HandleException(allowed_exceptions, on_exception)

    def and_reraise(self, allowed_exceptions,
                    msg="Logging error and reraising",
                    level=logging.ERROR, exc_info=True, stacklevel=3):
        """Context manager that logs and reraises given error.

        Arguments:
            allowed_exceptions: Exception(s) to log before reraising.
            msg: Message logged for exceptions.
            level: Logging level for logging exceptions.
            exc_info: If True, include exception info.
            stacklevel: Stacklevel of logging statement. Defaults to level 3
                since this method (level=2) defers functionality to a helper
                utility (level=1), but logging should use the context where
                this is called (level=3).
        """
        def on_exception():
            with self.temp_monkey_patched_logger():
                self.log(level, msg, exc_info=exc_info, stacklevel=stacklevel)
            raise

        return utils.HandleException(allowed_exceptions, on_exception)
