import logging
import mock

import pytest

from .. import logmanager


class TestLogManager:

    def setup(self):
        self.logger = mock.Mock(spec=logging.Logger)
        self.log = logmanager.LogManager(self.logger)

    def test_log(self):
        self.log.log(logging.INFO, 'info msg')
        self.logger.log.assert_called_once_with(logging.INFO, 'info msg')

    @pytest.mark.parametrize('level', [
        'debug',
        'info',
        'warn',
        'warning',
        'error',
        'exception',
        'fatal',
        'critical',
    ])
    def test_delegate_to_logger(self, level):
        log_method = getattr(self.log, level)
        base_log_method = getattr(self.logger, level)

        log_method('info msg')
        base_log_method.assert_called_once_with('info msg')
