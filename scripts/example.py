#!/usr/bin/env python
"""
Description
"""
import argparse
import logging

from logquacious import LogManager


LOG_FORMATS = {
    'default':
        '%(asctime)s %(levelname)-8s %(pathname)s:%(lineno)s %(message)s',
    'simple': '[%(levelname)s] %(message)s',
}


def example():
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



def main():
    formatter = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=formatter)
    parser.add_argument('--format', default='default',
                        choices=LOG_FORMATS.keys(),
                        help="Log format string used for example.")

    args = parser.parse_args()

    format_string = LOG_FORMATS[args.format]
    logging.basicConfig(format=format_string, level=logging.DEBUG)
    example()


if __name__ == '__main__':
    main()
