import logging

from logquacious import LogManager


logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)

log = LogManager(__name__)


with log.context.debug('greetings'):
    print('Hello!')


@log.context.info
def divide(numerator, denominator):
    if denominator == 0:
        log.warning('Attempted division by zero. Returning None')
        return None
    return numerator / denominator


divide(1, 0)


with log.and_suppress(ValueError, msg="It's ok, mistakes happen"):
    raise ValueError('Test error')


log = LogManager(__name__, context_templates={
    'function.start': 'Called `{label}({arguments})`',
    'function.finish': 'Return from `{label}`',
    'context.start.ERROR': '=============== Enter {label} ===============',
    'context.finish.ERROR': '=============== Exit {label} ===============',
})


@log.context.info
def no_op():
    pass

no_op()


@log.context.info(show_args=True)
def func_with_args(*args):
    pass

func_with_args('a', 1)

with log.context.error('error context'):
    print('This should never have happened! What did you do?')


log = LogManager(__name__, context_templates={
    'context.start': '=============== Enter {label} ===============',
    'context.finish': '=============== Exit {label} ===============',
})

with log.context.debug('greetings'):
    print('Hello!')
