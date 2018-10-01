from logquacious import utils


SHOW_ALL = {'show_args': True, 'show_kwargs': True}

#: Shortcut for `utils.format_function_args`
_format_func_args = utils.format_function_args


class TestFormatFunctionArgs:

    def test_empty_args_and_kwargs(self):
        assert _format_func_args((), {}, **SHOW_ALL) == ''

    def test_defaults_to_show_none(self):
        assert _format_func_args(['arg'], {'a': 1}) == ''

    def test_show_args(self):
        assert _format_func_args('ab', {}, **SHOW_ALL) == "'a', 'b'"

    def test_show_kwargs(self):
        assert _format_func_args((), {'a': 1}, **SHOW_ALL) == "a=1"

    def test_show_kwargs_repr(self):
        assert _format_func_args((), {'a': 'hello'}, **SHOW_ALL) == "a='hello'"

    def test_show_args_and_kwargs(self):
        assert _format_func_args(['a'], {'b': 1}, **SHOW_ALL) == "'a', b=1"

    def test_show_args_not_kwargs(self):
        assert _format_func_args(['a'], {'b': 1}, show_args=True) == "'a'"

    def test_show_kwargs_not_args(self):
        assert _format_func_args(['a'], {'b': 1}, show_kwargs=True) == "b=1"
