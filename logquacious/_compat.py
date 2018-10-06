import functools
import sys

if (sys.version_info > (3, 0)):
    from collections.abc import Mapping
    from contextlib import ContextDecorator
else:
    from collections import Mapping

    class ContextDecorator(object):
        def __call__(self, f):
            @functools.wraps(f)
            def decorated(*args, **kwargs):
                with self:
                    return f(*args, **kwargs)
            return decorated


__all__ = [
    'ContextDecorator',
    'Mapping',
]
