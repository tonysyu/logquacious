import functools
import logging

from . import utils
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


class _BaseContextLogger(object):

    context_type = None

    def __init__(self, templates, logger, log_level=logging.INFO, label=None):
        self.logger = utils.get_logger(logger)
        self.log_level = log_level
        self.label = label

        level_name = logging.getLevelName(log_level)
        start_key = '{}.start.{}'.format(self.context_type, level_name)
        self.start_template = templates.get(start_key)
        finish_key = '{}.finish.{}'.format(self.context_type, level_name)
        self.finish_template = templates.get(finish_key)

    def log(self, msg, *args, **kwargs):
        self.logger.log(self.log_level, msg, *args, **kwargs)


class ContextLogger(_BaseContextLogger):

    context_type = 'context'

    def __init__(self, templates, logger, log_level=logging.INFO, label=None):
        super(ContextLogger, self).__init__(templates, logger,
                                            log_level=log_level, label=label)

    def __enter__(self):
        self.log(self.start_template.format(label=self.label))

    def __exit__(self, *args, **kwds):
        self.log(self.finish_template.format(label=self.label))


class FunctionContextLogger(_BaseContextLogger):

    context_type = 'function'

    def __init__(self, templates, logger, log_level=logging.INFO, label=None,
                 show_args=False, show_kwargs=False):
        super(FunctionContextLogger, self).__init__(
            templates, logger, log_level=log_level, label=label
        )
        self._format_function_args = functools.partial(
            utils.format_function_args,
            show_args=show_args,
            show_kwargs=show_kwargs,
        )

    def __call__(self, func):
        self.label = func.__name__

        @functools.wraps(func)
        def decorated(*args, **kwargs):
            arg_string = self._format_function_args(args, kwargs)
            log_kwargs = {'label': self.label, 'arguments': arg_string}

            self.log(self.start_template.format(**log_kwargs))
            output = func(*args, **kwargs)
            self.log(self.finish_template.format(**log_kwargs))

            return output

        return decorated


class _ContextLoggerFactory:
    """Factory returning a `_ContextLogger` for a specific logging level.

    Note that each use as a context manager or decorator
    """

    def __init__(self, logger, log_level, templates):
        self.logger = utils.get_logger(logger)
        self.log_level = log_level
        self.templates = templates

    def __call__(self, func_or_label=None, show_args=False, show_kwargs=False):
        if func_or_label is None or callable(func_or_label):
            decorator = FunctionContextLogger(
                templates=self.templates,
                logger=self.logger,
                log_level=self.log_level,
                show_args=show_args,
                show_kwargs=show_kwargs,
            )
            if func_or_label is None:
                return decorator
            # Decorator called without arguments so argument is function.
            return decorator(func_or_label)
        return ContextLogger(
            templates=self.templates,
            logger=self.logger,
            log_level=self.log_level,
            label=func_or_label,
        )
