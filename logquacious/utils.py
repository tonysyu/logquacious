import logging


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
