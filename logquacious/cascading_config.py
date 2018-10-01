from collections import deque

from ._compat import Mapping
from .utils import is_sequence


class CascadingConfig(Mapping):
    """Cascading configuration values.

    This class allows you to define parameter names that can match exactly, but
    if it doesn't, parameter names will be searched as defined by
    `cascade_map`. `cascade_map` basically defines edges of a dependency graph,
    which is then used for a breadth-first search of parameter values.

    Parameters
    ----------
    config_values : dict or list of (key, value) pairs
        Default values for a configuration, where keys are the parameter names
        and values are the associated value.
    cascade_map : dict
        Dictionary defining cascading defaults. If a parameter name is not
        found, indexing `cascade_map` with the parameter name will return
        the parameter to look for.
    kwargs : dict
        Keyword arguments for initializing dict.
    """
    def __init__(self, config_values=None, cascade_map=None):
        if config_values is None:
            config_values = {}

        self._config_values = config_values.copy()

        if cascade_map is None:
            cascade_map = {}
        self.cascade_map = cascade_map.copy()

    def __getitem__(self, key):
        return self._config_values[key]

    def __iter__(self):
        return self._config_values.__iter__()

    def __len__(self):
        return len(self._config_values)

    def get(self, name, default=None, _prev=None):
        """Return best matching config value for `name`.

        Get value from configuration. The search for `name` is in the following
        order:

            - `self` (Value in global configuration)
            - `default`
            - Alternate name specified by `self.cascade_map`

        This method supports the pattern commonly used for optional keyword
        arguments to a function. For example::

            >>> def print_value(key, **kwargs):
            ...     print(kwargs.get(key, 0))
            >>> print_value('a')
            0
            >>> print_value('a', a=1)
            1

        Instead, you would create a config class and write::

            >>> config = CascadingConfig({'a': 0})
            >>> def print_value(key, **kwargs):
            ...     print(kwargs.get(key, config.get(key)))
            >>> print_value('a')
            0
            >>> print_value('a', a=1)
            1
            >>> print_value('b')
            None
            >>> config.cascade_map['b'] = 'a'
            >>> print_value('b')
            0

        See examples below for a demonstration of the cascading of
        configuration names.

        Parameters
        ----------
        name : str
            Name of config value you want.
        default : object
            Default value if name doesn't exist in instance.

        Examples
        --------
        >>> config = CascadingConfig({'size': 0},
        ...                          cascade_map={'arrow.size': 'size'})
        >>> config.get('size')
        0
        >>> top_choice = {'size': 1}
        >>> top_choice.get('size', config.get('size'))
        1
        >>> config.get('non-existent', 'unknown')
        'unknown'
        >>> config.get('arrow.size')
        0
        >>> config.get('arrow.size', 2)
        2
        >>> top_choice.get('size', config.get('arrow.size'))
        1
        """
        if name in self:
            return self._config_values[name]
        elif default is not None:
            return default
        elif name not in self.cascade_map:
            return None
        else:
            for name in self._iter_names(name):
                if name in self:
                    return self._config_values[name]

    def cascade_list(self, name):
        """Return list of cascade hierarchy for a given configuration name."""
        return list(self._iter_names(name))

    def cascade_path(self, name):
        """Return string of describing cascade."""
        return ' -> '.join(self.cascade_list(name))

    def __missing__(self, name):
        return None

    def _iter_names(self, name):
        visited = set()
        q = deque()

        def not_visited(key):
            return key not in visited and key not in q

        def update_queue(name):
            if name in self.cascade_map:
                children = self.cascade_map[name]
                if is_sequence(children):
                    q.extend(filter(not_visited, children))
                elif not_visited(children):
                    q.append(children)

        q.append(name)
        while q:
            name = q.popleft()
            yield name
            visited.add(name)
            update_queue(name)
