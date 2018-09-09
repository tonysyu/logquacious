class CascadingConfig(dict):
    """Cascading configuration values.

    This class allows you to define parameter names that can match exactly, but
    if it doesn't, parameter names will be searched as defined by
    `cascade_map`.

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
    def __init__(self, config_values=None, cascade_map=None, **kwargs):
        assert 'cascade_map' not in kwargs
        assert 'config_values' not in kwargs

        if config_values is None:
            config_values = {}

        super(CascadingConfig, self).__init__(config_values, **kwargs)

        if cascade_map is None:
            cascade_map = {}
        self.cascade_map = cascade_map

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

            >>> config = CascadingConfig(a=0)
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
        >>> top_choice={'size': 1}
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
            return self[name]
        elif default is not None:
            return default
        elif name not in self.cascade_map:
            return None
        else:
            _prev = _append_to_cascade(name, _prev)
            return self.get(self.cascade_map[name], _prev=_prev)

    def cascade_list(self, name, _prev=None):
        """Return list of cascade hierarchy for a given configuration name."""
        path = []
        while True:
            path = _append_to_cascade(name, path)
            try:
                name = self.cascade_map[name]
            except KeyError:
                break
        return path

    def cascade_path(self, name):
        """Return string of describing cascade."""
        return ' -> '.join(self.cascade_list(name))

    def __missing__(self, name):
        return None


def _append_to_cascade(name, previous=None):
    """Append name to previous nodes in configuration cascade.

    If name is already in the previous steps of the cascade, raise an error
    to indicate a circular dependence.
    """
    if previous is None:
        previous = []

    if name in previous:
        msg = '`cascade_map` defines circular dependency: {}'
        raise KeyError(msg.format(' -> '.join(previous + [name])))

    previous.append(name)
    return previous
