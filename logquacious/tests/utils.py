class StartsWith(str):

    def __eq__(self, other):
        if hasattr(other, 'startswith'):
            return other.startswith(self)
        return False
