===========
logquacious
===========

.. default-role:: literal

.. image:: https://img.shields.io/pypi/v/logquacious.svg
    :target: https://pypi.python.org/pypi/logquacious

.. image:: https://travis-ci.com/tonysyu/logquacious.svg?branch=master
    :target: https://travis-ci.com/tonysyu/logquacious

.. image:: https://readthedocs.org/projects/logquacious/badge/?version=latest
    :target: https://logquacious.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/tonysyu/logquacious/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/tonysyu/logquacious


Logquacious is a set of simple logging utilities to help you over-communicate.
(Logorrhea would've been a good name, if it didn't sound so terrible.)

Good application logging is easy to overlook, until you have to debug an error
in production. Logquacious aims to make logging as easy as possible. You can
find read more at the official `ReadTheDocs documentation`_.

Quick start
-----------

To get started, first make sure logquacious is installed::

    $ pip install logquacious

You'll also need to set up logging for your application. For this
example, we'll use a really simple configuration:

.. code-block:: python

    import logging

    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=logging.DEBUG)

Note that this simple configuration is used for demonstration purposes, only.
See the `Logging Cookbook`_ in the official Python docs for examples of
options used for real logging configuration.

The main interface to `logquacious` is the `LogManager`, which can be used for
normal logging:

.. code-block:: python

    import logquacious

    log = logquacious.LogManager(__name__)

.. ignore-next-block
.. code-block:: python

    log.debug('Nothing to see here.')

Due to our simplified logging format defined earlier, that would output:

.. code-block:: console

    DEBUG: Nothing to see here.

That isn't a very interesting example. In addition to basic logging,
`LogManager` has a `context` attribute for use as a context manager:

.. code-block:: python

    >>> with log.context.debug('greetings'):
    ...    print('Hello!')
    DEBUG: Enter greetings
    Hello!
    DEBUG: Exit greetings

The same attribute can be used as a decorator, as well:

.. code-block:: python

    @log.context.info
    def divide(numerator, denominator):
        if denominator == 0:
            log.warning('Attempted division by zero. Returning None')
            return None
        return numerator / denominator

    >>> divide(1, 0)
    INFO: Call `divide()`
    WARNING: Attempted division by zero. Returning None
    INFO: Return from `divide`

Even better, you can log input arguments as well:

.. code-block:: python

    @log.context.info(show_args=True, show_kwargs=True)
    def greet(name, char='-'):
        msg = 'Hello, {name}'.format(name=name)
        print(msg)
        print(char * len(msg))

    >>> greet('Tony', char='~')
    INFO: Call `greet('Tony', char='~')`
    Hello, Tony
    ~~~~~~~~~~~
    INFO: Return from `greet`

There's also a special context manager for suppressing errors and logging:

.. code-block:: python

    with log.and_suppress(ValueError, msg="It's ok, mistakes happen"):
        raise ValueError('Test error')

.. code-block:: console

    [ERROR] It's ok, mistakes happen
    Traceback (most recent call last):
      File "/Users/tyu/code/logquacious/logquacious/log_manager.py", line 103, in and_suppress
        yield
      File "scripts/example.py", line 26, in <module>
        raise ValueError('Test error')
    ValueError: Test error

Note the traceback above is logged, not streamed to stderr.


Configuration
-------------

The message templates used by `LogManager.context` can be configured to your
liking by passing a `context_templates` argument to `LogManager`:

.. code-block:: python

    log = logquacious.LogManager(__name__, context_templates={
        'context.start': '=============== Enter {label} ===============',
        'context.finish': '=============== Exit {label} ===============',
    })

    with log.context.debug('greetings'):
        print('Hello!')

.. code-block:: console

    [DEBUG] =============== Enter greetings ===============
    Hello!
    [DEBUG] =============== Exit greetings ===============


The general format for `context_templates` keys is::

    [CONTEXT_TYPE.]('start'|'finish')[.LOG_LEVEL_NAME]

where square-brackes marks optional fields.

`CONTEXT_TYPE` can be any of the following:

- `function`: Template used when called as a decorator.
- `context`: Template used when called as a context manager.

`LOG_LEVEL_NAME` can be any of the following logging levels:

- `DEBUG`
- `INFO`
- `WARNING`
- `ERROR`
- `CRITICAL`

For example, consider the cascade graph for `function.start.DEBUG`, which
looks like::

                    function.start.DEBUG
                         /       \
               start.DEBUG       function.start
                         \       /
                           start

The cascade is performed using a breadth-first search. If
`function.start.DEBUG` is not defined, check `start.DEBUG` then check
`function.start` *BEFORE* checking `start`.

The default configuration is:

.. code-block:: python

    DEFAULT_TEMPLATES = {
        'start': 'Enter {label}',
        'finish': 'Exit {label}',
        'function.start': 'Call `{label}({arguments})`',
        'function.finish': 'Return from `{label}`',
    }

Note that custom configuration *updates* these defaults. For example, if you
want to if you want to skip logging on exit for all context managers and
decorators, you'll have set *both* `'finish'` and `'function.finish'` to `None`
or an empty string.

As you can see above, two template variables may be passed to the template
string: `label` and `arguments`. When called as a context manager, the `label`
is the first argument to the context manager and `arguments` is always empty.
When called as a decorator, `label` is the function's `__name__` and
`arguments` a string representing input arguments, if `show_args` or
`show_kwargs` parameters are `True`.

Credits
-------

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.


.. _ReadTheDocs documentation: https://logquacious.readthedocs.io/en/latest/
.. _Logging Cookbook: https://docs.python.org/3.6/howto/logging-cookbook.html
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
