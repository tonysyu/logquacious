import logging


def get_logger(name_or_logger):
    if isinstance(name_or_logger, logging.Logger):
        return name_or_logger
    return logging.getLogger(name_or_logger)
