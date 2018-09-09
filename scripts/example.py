import logging

from logquacious import LogManager


log = LogManager(__name__)
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)


with log.context.debug('greetings'):
    print('Hello!')


@log.context.info
def divide(numerator, denominator):
    if denominator == 0:
        log.warn('Attempted division by zero. Returning None')
        return None
    return numerator / denominator


divide(1, 0)
