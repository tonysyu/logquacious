from logquacious.cascading_config import CascadingConfig


def test_get_simple():
    config = CascadingConfig({'size': 0})
    assert config.get('size') == 0


def test_get_default():
    config = CascadingConfig()
    assert config.get('size', 10) == 10


def test_get_best():
    cascade_map = {'font.size': 'size'}
    config = CascadingConfig({'size': 0, 'font.size': 1}, cascade_map)
    assert config.get('font.size') == 1


def test_get_cascade():
    config = CascadingConfig({'size': 0}, {'font.size': 'size'})
    assert config.get('font.size') == 0


def test_get_cascade_multi():
    cascade_map = {'font.size': 'size', 'div.font.size': 'font.size'}
    config = CascadingConfig({'size': 42}, cascade_map)
    assert config.get('font.size') == 42
    assert config.get('div.font.size') == 42


def test_cascade_path():
    config = CascadingConfig({}, {'font.size': 'size'})
    assert config.cascade_path('font.size') == 'font.size -> size'


def test_cascade_path_diamond_graph():
    config = CascadingConfig({}, {
        'class.font.size': ['div.font.size', 'font.size'],
        'div.font.size': 'size',
        'font.size': 'size',
    })
    assert (config.cascade_path('class.font.size') ==
            'class.font.size -> div.font.size -> font.size -> size')


def test_get_circular_cascade():
    config = CascadingConfig({'size': 42},
                             {'font.size': 'size', 'size': 'font.size'})
    assert config.get('size') == 42
    assert config.get('font.size') == 42


def test_list_circular_cascade():
    config = CascadingConfig({}, {'font.size': 'size', 'size': 'font.size'})
    assert config.cascade_path('size') == 'size -> font.size'
    assert config.cascade_path('font.size') == 'font.size -> size'
