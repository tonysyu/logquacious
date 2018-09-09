import itertools

import pytest

from .. import constants
from ..context_templates import ContextTemplates


CONTEXT_TYPES = ['function', 'context']
START_LEVEL_TEMPLATES = [
    'start.{}',
    'function.start.{}',
    'context.start.{}',
]
FINISH_LEVEL_TEMPLATES = [
    'finish.{}',
    'function.finish.{}',
    'context.finish.{}',
]
#: Config level keys for start: ['start.DEBUG', 'start.INFO',... ]
BASE_START_LEVEL_KEYS = [
    'start.{}'.format(name) for name in constants.LOG_LEVEL_NAMES
]
#: Config level keys for finish: ['finish.DEBUG', 'finish.INFO',... ]
BASE_FINISH_LEVEL_KEYS = [
    'finish.{}'.format(name) for name in constants.LOG_LEVEL_NAMES
]
#: Basic config keys for start: ['start', 'start.DEBUG',... ]
BASE_START_KEYS = ['start'] + BASE_START_LEVEL_KEYS
#: Basic config keys for finish: ['finish', 'finish.DEBUG',... ]
BASE_FINISH_KEYS = ['finish'] + BASE_FINISH_LEVEL_KEYS
#: Config keys for start: ['start', 'start.DEBUG', 'function.start',... ]
START_KEYS = BASE_START_KEYS + [
    '{}.{}'.format(prefix, name)
    for prefix, name in itertools.product(CONTEXT_TYPES, BASE_START_KEYS)
]
#: Config keys for finish: ['finish', 'finish.DEBUG', 'function.finish',... ]
FINISH_KEYS = BASE_FINISH_KEYS + [
    '{}.{}'.format(prefix, name)
    for prefix, name in itertools.product(CONTEXT_TYPES, BASE_FINISH_KEYS)
]


class TestMinimalLogContextConfig:

    def setup(self):
        self.start_text = '__start__'
        self.finish_text = '__finish__'
        self.config = ContextTemplates({
            'start': self.start_text,
            'finish': self.finish_text,
        })

    @pytest.mark.parametrize('key', START_KEYS)
    def test_start(self, key):
        assert self.config.get(key) == self.start_text

    @pytest.mark.parametrize('key', FINISH_KEYS)
    def test_finish(self, key):
        assert self.config.get(key) == self.finish_text


class TestLevelSpecificLogContextConfig:

    def setup(self):
        self.start_template = 'Start {}'
        self.finish_template = 'Finish {}'
        config_dict = {
            'start': 'ignore',
            'finish': 'ignore',
        }
        config_dict.update({
            'start.{}'.format(level): self.start_template.format(level)
            for level in constants.LOG_LEVEL_NAMES
        })
        config_dict.update({
            'finish.{}'.format(level): self.finish_template.format(level)
            for level in constants.LOG_LEVEL_NAMES
        })
        self.config = ContextTemplates(config_dict)

    @pytest.mark.parametrize('level', constants.LOG_LEVEL_NAMES)
    def test_start(self, level):
        for template in START_LEVEL_TEMPLATES:
            key = template.format(level)
            assert self.config.get(key) == self.start_template.format(level)

    @pytest.mark.parametrize('level', constants.LOG_LEVEL_NAMES)
    def test_finish(self, level):
        for template in FINISH_LEVEL_TEMPLATES:
            key = template.format(level)
            assert self.config.get(key) == self.finish_template.format(level)
