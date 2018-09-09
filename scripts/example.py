import logging

from logquacious import LogManager


logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)

log = LogManager(__name__, templates={
    'start': 'Start {label}',
    'finish': 'Finish {label}',
    'context.start.ERROR': '=============== Enter {label} ===============',
    'context.finish.ERROR': '=============== Exit {label} ===============',
})


with log.context.debug('greetings'):
    print('Hello!')


@log.context.info
def divide(numerator, denominator):
    if denominator == 0:
        log.warn('Attempted division by zero. Returning None')
        return None
    return numerator / denominator


divide(1, 0)


with log.context.error('error context'):
    print('This should never have happened! What did you do?')


with log.and_suppress(ValueError, msg="It's ok, mistakes happen"):
    raise ValueError('Test error')
