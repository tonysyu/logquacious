import logging
from unittest import TestCase

from logquacious.backport_configurable_stacklevel import PatchedLoggerMixin


class RecordingHandler(logging.NullHandler):

    def __init__(self, *args, **kwargs):
        super(RecordingHandler, self).__init__(*args, **kwargs)
        self.records = []

    def handle(self, record):
        """Keep track of all the emitted records."""
        self.records.append(record)


class TestPatchedLoggerMixin(PatchedLoggerMixin, TestCase):
    """TestCase for PatchedLoggerMixin adapted from cpython logger tests.

    Adapted from `LoggerTest` class of cpython logger tests.

    See https://github.com/python/cpython/blob/master/Lib/test/test_logging.py
    """

    def setUp(self):
        self.logger = logging.Logger(name='test')
        self.recording = RecordingHandler()
        self.logger.addHandler(self.recording)
        self.addCleanup(self.logger.removeHandler, self.recording)
        self.addCleanup(self.recording.close)
        self.addCleanup(logging.shutdown)

    def test_find_caller_with_stacklevel(self):
        """Test of PatchedLoggerMixin adapted from cpython logger tests.

        See https://github.com/python/cpython/pull/7424
        """
        the_level = 1

        def innermost():
            with self.temp_monkey_patched_logger():
                self.logger.warning('test', stacklevel=the_level)

        def inner():
            innermost()

        def outer():
            inner()

        records = self.recording.records

        outer()
        record_1 = records[-1]
        assert record_1.funcName == 'innermost'

        the_level = 2
        outer()
        stacklevel_2 = records[-1]
        assert stacklevel_2.funcName == 'inner'
        assert stacklevel_2.lineno > record_1.lineno

        the_level = 3
        outer()
        stacklevel_3 = records[-1]
        assert stacklevel_3.funcName == 'outer'
        assert stacklevel_3.lineno > stacklevel_2.lineno

        the_level = 4
        outer()
        stacklevel_4 = records[-1]
        assert stacklevel_4.funcName == 'test_find_caller_with_stacklevel'
        assert stacklevel_4.lineno > stacklevel_3.lineno
