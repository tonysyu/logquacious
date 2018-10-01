import sys

if (sys.version_info > (3, 0)):
    from collections.abc import Mapping
else:
    from collections import Mapping


__all__ = [
    'Mapping',
]
