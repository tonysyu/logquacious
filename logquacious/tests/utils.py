from ..utils import is_string


class StartsWith(str):

    def __eq__(self, other):
        if is_string(other):
            return other.startswith(self)
        return False
