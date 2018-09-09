import logging
from collections import defaultdict

from . import utils
from ._compat import ContextDecorator


__all__ = ['LogContext']


class LogContext:
    """Manager for context managers/decorators used for logging.

    Attributes:
        debug: Decortor/context-manager with level logging.DEBUG.
        info: Decortor/context-manager with level logging.INFO.
        warn: Decortor/context-manager with level logging.WARNING.
        warning: Decortor/context-manager with level logging.WARNING.
        error: Decortor/context-manager with level logging.ERROR.
        fatal: Decortor/context-manager with level logging.CRITICAL.
        critical: Decortor/context-manager with level logging.CRITICAL.
    """

    def __init__(self, logger, config=None):
        self.logger = utils.get_logger(logger)
        self.debug = _ContextLoggerFactory(logger, logging.DEBUG, config)
        self.info = _ContextLoggerFactory(logger, logging.INFO, config)
        self.warn = _ContextLoggerFactory(logger, logging.WARNING, config)
        self.warning = _ContextLoggerFactory(logger, logging.WARNING, config)
        self.error = _ContextLoggerFactory(logger, logging.ERROR, config)
        self.fatal = _ContextLoggerFactory(logger, logging.CRITICAL, config)
        self.critical = _ContextLoggerFactory(logger, logging.CRITICAL, config)


class _ContextLogger(ContextDecorator):

    def __init__(self, logger, log_level, label, templates):
        self.logger = utils.get_logger(logger)
        self.log_level = log_level
        self.label = label
        self.start_template = templates.start[log_level]
        self.finish_template = templates.finish[log_level]

    def __enter__(self):
        self.log(self.start_template.format(label=self.label))

    def __exit__(self, *args, **kwds):
        self.log(self.finish_template.format(label=self.label))

    def log(self, msg, *args, **kwargs):
        self.logger.log(self.log_level, msg, *args, **kwargs)


class _ContextLoggerFactory:
    """Factory returning a `_ContextLogger` for a specific logging level.

    Note that each use as a context manager or decorator
    """

    def __init__(self, logger, log_level, config):
        self.logger = utils.get_logger(logger)
        self.log_level = log_level
        self.config = config

    def __call__(self, func_or_label):
        if callable(func_or_label):
            label = func_or_label.__name__
            return self._create_logging_decorator(func_or_label, label)
        templates = ContextTemplates()
        return self._create_context_logger(func_or_label, templates)

    def _create_logging_decorator(self, func, label, **kwargs):
        templates = ContextTemplates()
        return self._create_context_logger(label, templates)(func)

    def _create_context_logger(self, label, templates):
        return _ContextLogger(
            logger=self.logger,
            log_level=self.log_level,
            label=label,
            templates=templates,
        )


class ContextTemplates:

    def __init__(self):
        self.start = defaultdict(lambda: 'Start {label}')
        self.finish = defaultdict(lambda: 'Finish {label}')
