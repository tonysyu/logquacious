import logging
import mock

import pytest

from logquacious import log_context


logging.basicConfig()


func_name_and_level_parameters = pytest.mark.parametrize('func_name, level', [
    ('debug', logging.DEBUG),
    ('info', logging.INFO),
    ('warning', logging.WARNING),
    ('error', logging.ERROR),
    ('fatal', logging.CRITICAL),
])


class TestLogContext:

    def setup(self):
        self.logger = mock.Mock(spec=logging.Logger)
        self.context = log_context.LogContext(self.logger)

    @func_name_and_level_parameters
    def test_context_delegates_to_logger(self, func_name, level):
        context_manager = getattr(self.context, func_name)

        with context_manager('context label'):
            pass

        self.logger.log.assert_has_calls([
            mock.call(level, 'Enter context label', stacklevel=3),
            mock.call(level, 'Exit context label', stacklevel=3),
        ])

    @func_name_and_level_parameters
    def test_decorator_delegates_to_logger(self, func_name, level):
        decorator = getattr(self.context, func_name)

        @decorator
        def function():
            pass

        # Decorating the function shouldn't log anything.
        self.logger.log.assert_not_called()

        function()

        self.logger.log.assert_has_calls([
            mock.call(level, 'Call `function()`', stacklevel=3),
            mock.call(level, 'Return from `function`', stacklevel=3),
        ])

    @func_name_and_level_parameters
    def test_decorator_with_args_delegates_to_logger(self, func_name, level):
        context = log_context.LogContext(self.logger, templates={
            'function.start': 'Called `{label}({arguments})`',
            'function.finish': 'Return from `{label}`',
        })
        decorator = getattr(context, func_name)

        @decorator(show_args=True, show_kwargs=True)
        def function(a, b=None):
            pass

        # Decorating the function shouldn't log anything.
        self.logger.log.assert_not_called()

        function('a', b=1)

        self.logger.log.assert_has_calls([
            mock.call(level, "Called `function('a', b=1)`", stacklevel=3),
            mock.call(level, 'Return from `function`', stacklevel=3),
        ])

    @func_name_and_level_parameters
    def test_null_start_template_for_decorator(self, func_name, level):
        context = log_context.LogContext(self.logger, templates={
            'function.start': '',
            'function.finish': 'Finish',
        })
        decorator = getattr(context, func_name)

        @decorator
        def function():
            pass

        function()

        self.logger.log.assert_called_once_with(level, "Finish", stacklevel=3)

    @func_name_and_level_parameters
    def test_null_finish_template_for_decorator(self, func_name, level):
        context = log_context.LogContext(self.logger, templates={
            'function.start': 'Start',
            'function.finish': '',
        })
        decorator = getattr(context, func_name)

        @decorator
        def function():
            pass

        function()

        self.logger.log.assert_called_once_with(level, "Start", stacklevel=3)

    @func_name_and_level_parameters
    def test_null_start_template_for_context_manager(self, func_name, level):
        context = log_context.LogContext(self.logger, templates={
            'context.start': '',
            'context.finish': 'Finish',
        })

        context_manager = getattr(context, func_name)

        with context_manager('context label'):
            pass

        self.logger.log.assert_called_once_with(level, "Finish", stacklevel=3)

    @func_name_and_level_parameters
    def test_null_finish_template_for_context_manager(self, func_name, level):
        context = log_context.LogContext(self.logger, templates={
            'context.start': 'Start',
            'context.finish': '',
        })

        context_manager = getattr(context, func_name)

        with context_manager('context label'):
            pass

        self.logger.log.assert_called_once_with(level, "Start", stacklevel=3)
