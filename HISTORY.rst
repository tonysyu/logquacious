=======
History
=======

0.5.0 (2019-05-05)
------------------

- Backport `stacklevel` keyword argument from Python 3.8 and configure
  stacklevel such that logging utilities report the context (e.g. filename
  and line number) where `logquacious` utilities are called.

0.4.0 (2018-10-05)
------------------

- Fix config override behavior to extend rather than replace default templates

0.3.0 (2018-10-05)
------------------

- Add decorator support for `log.and_suppress` and `log.and_reraise` context
  managers
- Suppress logging for null/empty log message templates


0.2.0 (2018-10-03)
------------------

Changed default templates. In 0.1.0, the templates were:

.. code:: python

    DEFAULT_TEMPLATES = {
        'start': 'Start {label}',
        'finish': 'Finish {label}',
    }


These defaults have been changed to:

.. code:: python

    DEFAULT_TEMPLATES = {
        'start': 'Enter {label}',
        'finish': 'Exit {label}',
        'function.start': 'Call `{label}({arguments})`',
        'function.finish': 'Return from `{label}`',
    }

0.1.0 (2018-10-03)
------------------

* First release on PyPI.
