import logging

from . import utils
from ._compat import ContextDecorator
from .context_templates import ContextTemplates


__all__ = ['LogContext']


class LogContext:
    """Manager for context managers/decorators used for logging.

    Attributes:
        debug: Decortor/context-manager with level logging.DEBUG.
        info: Decortor/context-manager with level logging.INFO.
        warning: Decortor/context-manager with level logging.WARNING.
        error: Decortor/context-manager with level logging.ERROR.
        fatal: Decortor/context-manager with level logging.CRITICAL.
    """

    def __init__(self, logger, templates=None):
        templates = ContextTemplates.resolve(templates)
        self.logger = utils.get_logger(logger)
        self.debug = _ContextLoggerFactory(logger, logging.DEBUG, templates)
        self.info = _ContextLoggerFactory(logger, logging.INFO, templates)
        self.warning = _ContextLoggerFactory(logger, logging.WARNING, templates)  # noqa: E501
        self.error = _ContextLoggerFactory(logger, logging.ERROR, templates)
        self.fatal = _ContextLoggerFactory(logger, logging.CRITICAL, templates)


class _ContextLogger(ContextDecorator):

    def __init__(self, logger, log_level, label, context_type, templates):
        self.logger = utils.get_logger(logger)
        self.log_level = log_level
        self.label = label

        level_name = logging.getLevelName(log_level)
        start_key = '{}.start.{}'.format(context_type, level_name)
        self.start_template = templates.get(start_key)
        finish_key = '{}.finish.{}'.format(context_type, level_name)
        self.finish_template = templates.get(finish_key)

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

    def __init__(self, logger, log_level, templates):
        self.logger = utils.get_logger(logger)
        self.log_level = log_level
        self.templates = templates

    def __call__(self, func_or_label):
        if callable(func_or_label):
            label = func_or_label.__name__
            return self._create_logging_decorator(func_or_label, label,
                                                  'function')
        return self._create_context_logger(func_or_label, 'context')

    def _create_logging_decorator(self, func, label, context_type, **kwargs):
        return self._create_context_logger(label, context_type)(func)

    def _create_context_logger(self, label, context_type):
        return _ContextLogger(
            logger=self.logger,
            log_level=self.log_level,
            label=label,
            context_type=context_type,
            templates=self.templates,
        )
