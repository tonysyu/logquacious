import pytest

from ..cascading_config import CascadingConfig


def test_get_simple():
    config = CascadingConfig({'size': 0})
    assert config.get('size') == 0


def test_get_default():
    config = CascadingConfig()
    assert config.get('size', 10) == 10


def test_get_best():
    cascade_map = {'arrow.size': 'size'}
    config = CascadingConfig({'size': 0, 'arrow.size': 1}, cascade_map)
    assert config.get('arrow.size') == 1


def test_get_cascade():
    config = CascadingConfig({'size': 0}, {'arrow.size': 'size'})
    assert config.get('arrow.size') == 0


def test_get_cascade_multi():
    cascade_map = {'arrow.size': 'size', 'quiver.size': 'arrow.size'}
    config = CascadingConfig({'size': 42}, cascade_map)
    assert config.get('arrow.size') == 42
    assert config.get('quiver.size') == 42


def test_cascade_path():
    config = CascadingConfig({}, {'arrow.size': 'size'})
    assert config.cascade_path('arrow.size') == 'arrow.size -> size'


def test_get_circular_cascade():
    config = CascadingConfig({}, {'arrow.size': 'size', 'size': 'arrow.size'})
    with pytest.raises(KeyError):
        config.get('size')


def test_list_circular_cascade():
    config = CascadingConfig({}, {'arrow.size': 'size', 'size': 'arrow.size'})
    with pytest.raises(KeyError):
        config.cascade_list('size')
