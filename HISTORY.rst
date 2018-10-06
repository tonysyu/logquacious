=======
History
=======

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
