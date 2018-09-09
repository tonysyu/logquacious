try:
    from contextlib import ContextDecorator
except ImportError:
    import functools

    class ContextDecorator(object):
        def __call__(self, f):
            @functools.wraps(f)
            def decorated(*args, **kwargs):
                with self:
                    return f(*args, **kwargs)
            return decorated


__all__ = ['ContextDecorator']
