import logging


LOG_LEVEL_NAMES = [
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL',
]


LOG_LEVELS = {getattr(logging, name) for name in LOG_LEVEL_NAMES}
