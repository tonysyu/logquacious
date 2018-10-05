import itertools
import mock

import pytest

from logquacious import constants, context_templates
from logquacious.context_templates import DEFAULT_TEMPLATES, ContextTemplates
from utils import StartsWith


CONTEXT_TYPES = ['function', 'context']
STAGES = ['start', 'finish']
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


class TestContextTemplates:

    def test_config_missing_start(self):
        templates = ContextTemplates({'finish': 'custom'})
        assert templates['finish'] == 'custom'
        assert templates['start'] == DEFAULT_TEMPLATES['start']

    def test_config_missing_finish(self):
        templates = ContextTemplates({'start': 'custom'})
        assert templates['start'] == 'custom'
        assert templates['finish'] == DEFAULT_TEMPLATES['finish']

    def test_null_config(self):
        config = ContextTemplates()
        assert config == DEFAULT_TEMPLATES

    def test_unknown_config_key(self):
        with mock.patch.object(context_templates, '_LOG') as mock_log:
            ContextTemplates({'BAD-KEY': 'placeholder'})
        mock_log.warning.assert_called_once_with(
            StartsWith("%s given `config_dict` with unknown keys"),
            'ContextTemplates',
            mock.ANY,
        )


class TestMinimalContextTemplates:

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


class TestLevelSpecificContextTemplates:

    def setup(self):
        self.start_template = 'Start {}'
        self.finish_template = 'Finish {}'
        config_dict = {}
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


class TestSecondaryContextTemplates:
    """Test secondary cascade for context templates.

    For example, consider the cascade pattern for `function.start.DEBUG`.
    which has a cascade graph that looks like::

                        function.start.DEBUG
                             /       \
                   start.DEBUG       function.start
                             \       /
                               start

    The cascade is performed using a breadth-first search. If
    `function.start.DEBUG` is not defined, check `start.DEBUG` then check
    `function.start` *BEFORE* checking `start`. This test case only defines
    `function.start` (and similar values) to check this secondary cascade
    """

    def setup(self):
        self.config_keys = [
            '{}.{}'.format(context, stage)
            for context, stage in itertools.product(CONTEXT_TYPES, STAGES)
        ]
        self.config = ContextTemplates(
            {name: name for name in self.config_keys}
        )

    @pytest.mark.parametrize('context, stage, level', [
        args for args in itertools.product(
            CONTEXT_TYPES, STAGES, constants.LOG_LEVEL_NAMES,
        )
    ])
    def test_secondary_context_match(self, context, stage, level):
        key = '{}.{}.{}'.format(context, stage, level)
        assert self.config.get(key) == '{}.{}'.format(context, stage)
