import logging
from itertools import chain

from . import constants
from .cascading_config import CascadingConfig


__all__ = ['CASCADE_MAP', 'ContextTemplates']


_LOG = logging.getLogger(__name__)


def _build_cascade_map():
    start_cascade_map = {
        'start.{}'.format(name): 'start'
        for name in constants.LOG_LEVEL_NAMES
    }
    finish_cascade_map = {
        'finish.{}'.format(name): 'finish'
        for name in constants.LOG_LEVEL_NAMES
    }

    cascade_map = {
        'function.start': 'start',
        'context.start': 'start',
        'function.finish': 'finish',
        'context.finish': 'finish',
    }
    cascade_map.update({
        'function.{}'.format(name): [name, 'function.start']
        for name in start_cascade_map.keys()
    })
    cascade_map.update({
        'context.{}'.format(name): [name, 'context.start']
        for name in start_cascade_map.keys()
    })
    cascade_map.update({
        'function.{}'.format(name): [name, 'function.finish']
        for name in finish_cascade_map.keys()
    })
    cascade_map.update({
        'context.{}'.format(name): [name, 'context.finish']
        for name in finish_cascade_map.keys()
    })
    cascade_map.update(start_cascade_map)
    cascade_map.update(finish_cascade_map)
    return cascade_map


CASCADE_MAP = _build_cascade_map()


DEFAULT_TEMPLATES = {
    'start': 'Enter {label}',
    'finish': 'Exit {label}',
    'function.start': 'Call `{label}({arguments})`',
    'function.finish': 'Return from `{label}`',
}


class ContextTemplates(CascadingConfig):

    def __init__(self, config_dict=None):
        config_dict = config_dict or DEFAULT_TEMPLATES
        config_dict = config_dict.copy()
        config_dict.setdefault('start', DEFAULT_TEMPLATES['start'])
        config_dict.setdefault('finish', DEFAULT_TEMPLATES['finish'])
        self._warn_if_given_unknown_keys(config_dict.keys())

        super(ContextTemplates, self).__init__(config_dict, CASCADE_MAP)

    def _warn_if_given_unknown_keys(self, config_keys):
        known_keys = chain(CASCADE_MAP.keys(), ['start', 'finish'])
        unknown_keys = set(config_keys).difference(known_keys)
        if any(unknown_keys):
            _LOG.warning("%s given `config_dict` with unknown keys: %s",
                         self.__class__.__name__, unknown_keys)

    def __missing__(self, key):
        known_keys = set(chain(self.keys(), self.cascade_map.keys()))
        raise KeyError("Key {!r} not known key: {}".format(key, known_keys))

    @classmethod
    def resolve(cls, templates):
        if isinstance(templates, cls):
            return templates
        return cls(templates)
