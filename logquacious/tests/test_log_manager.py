import logging
import mock

import pytest

from logquacious import log_manager


class TestLogManager:

    def setup(self):
        self.logger = mock.Mock(spec=logging.Logger)
        self.log = log_manager.LogManager(self.logger)

    def test_log(self):
        self.log.log(logging.INFO, 'info msg')
        self.logger.log.assert_called_once_with(logging.INFO, 'info msg')

    @pytest.mark.parametrize('level', [
        'debug',
        'info',
        'warning',
        'error',
        'exception',
        'fatal',
    ])
    def test_delegate_to_logger(self, level):
        log_method = getattr(self.log, level)
        base_log_method = getattr(self.logger, level)

        log_method('info msg')
        base_log_method.assert_called_once_with('info msg')

    def test_log_and_suppress_context_manager(self):
        with self.log.and_suppress(ValueError):
            raise ValueError('Suppress me')

        self.logger.log.assert_called_once_with(
            logging.ERROR,
            "Suppressed error and logging",
            exc_info=True,
            stacklevel=3,
        )

    def test_log_and_suppress_decorator(self):
        @self.log.and_suppress(ValueError)
        def function():
            raise ValueError('Suppress me')

        function()

        self.logger.log.assert_called_once_with(
            logging.ERROR,
            "Suppressed error and logging",
            exc_info=True,
            stacklevel=3,
        )

    def test_log_and_reraise_context_manager(self):
        with pytest.raises(ValueError):
            with self.log.and_reraise(ValueError):
                raise ValueError('Test error')

        self.logger.log.assert_called_once_with(
            logging.ERROR,
            "Logging error and reraising",
            exc_info=True,
            stacklevel=3,
        )

    def test_log_and_reraise_decorator(self):
        @self.log.and_reraise(ValueError)
        def function():
            raise ValueError('Suppress me')

        with pytest.raises(ValueError):
            function()

        self.logger.log.assert_called_once_with(
            logging.ERROR,
            "Logging error and reraising",
            exc_info=True,
            stacklevel=3,
        )

    @pytest.mark.parametrize('method', [
        'and_suppress',
        'and_reraise',
    ])
    def test_context_managers_do_not_catch_other_exceptions(self, method):
        context_manager = getattr(self.log, method)
        with pytest.raises(ValueError):
            with context_manager(KeyError):
                raise ValueError('Not caught by log manager')
        self.logger.log.assert_not_called()
