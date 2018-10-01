import logging
from itertools import chain


def get_logger(name_or_logger):
    if isinstance(name_or_logger, logging.Logger):
        return name_or_logger
    return logging.getLogger(name_or_logger)


def is_string(value):
    return hasattr(value, 'strip')


def is_sequence(value):
    """Return True if value is a non-string sequence.

    See https://stackoverflow.com/a/1835259/260303
    """
    return (
        not is_string(value) and (
            hasattr(value, '__getitem__') or
            hasattr(value, '__iter__')
        )
    )


def format_function_args(args, kwargs,
                         show_args=False,
                         show_kwargs=False):
    if not (show_args or show_kwargs) or not (args or kwargs):
        return ''

    kv_pairs = (
        (
            "{key}={value!r}".format(key=key, value=value)
            for key, value in kwargs.items()
        )
        if show_kwargs else ()
    )
    args = (repr(a) for a in args) if show_args else ()
    return ', '.join(chain(args, kv_pairs))
