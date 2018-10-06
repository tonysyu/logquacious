from logquacious.utils import is_string


class StartsWith(str):

    def __eq__(self, other):
        if is_string(other):
            return other.startswith(self)
        return False


def assert_dict_match(actual, expected, keys=None):
    if keys is None:
        assert actual.keys() == expected.keys()
        keys = actual.keys()

    for k in keys:
        assert actual[k] == expected[k]
