===========
logquacious
===========


.. image:: https://img.shields.io/pypi/v/logquacious.svg
    :target: https://pypi.python.org/pypi/logquacious

.. image:: https://img.shields.io/travis/tonysyu/logquacious.svg
    :target: https://travis-ci.org/tonysyu/logquacious

.. image:: https://readthedocs.org/projects/logquacious/badge/?version=latest
    :target: https://logquacious.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Logquacious is a set of simple logging utilities to help you over-communicate.
(Logorrhea would've been a good name, if it didn't sound so terrible.)

Good application logging is easy to overlook, until you have to debug an error
in production. Logquacious aims to make logging as easy as possible.

Quick start
-----------

To get started, you'll need set up logging for your application. For this
example, we'll use a really simple configuration:

.. code-block:: python

    import logging

    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)

The main interface to `logquacious` is the `LogManager`, which can be used for
normal logging:

.. code-block:: python

    import logquacious

    log = logquacious.LogManager(__name__)
    log.debug('Nothing to see here.')

Due to our simplified logging format defined earlier, that would output:

.. code-block:: console

    [DEBUG] Nothing to see here.

That isn't a very interesting example. In addition to basic logging,
`LogManager` has a `context` attribute for use as a context manager:

.. code-block:: python

    with log.context.debug('greetings'):
        print('Hello!')

.. code-block:: console

    [DEBUG] Start greetings
    Hello!
    [DEBUG] Finish greetings

The same attribute can be used as a decorator, as well:

.. code-block:: python

    @log.context.info
    def divide(numerator, denominator):
        if denominator == 0:
            log.warn('Attempted division by zero. Returning None')
            return None
        return numerator / denominator

    divide(1, 0)

.. code-block:: console

    [INFO] Start divide
    [WARNING] Attempted division by zero. Returning None
    [INFO] Finish divide

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


Credits
-------

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
