import logging
import mock

import pytest

from .. import log_context


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
            mock.call(level, 'Start context label'),
            mock.call(level, 'Finish context label'),
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
            mock.call(level, 'Start function'),
            mock.call(level, 'Finish function'),
        ])
