# License: public domain (none)
# Orignal Author: Marcus Muller <znek@mulle-kybernetik.com>
# Included in Coils 2009-10-15
class StringBuffer:
        """
        A mutable string. This implementation is quite inefficient, but I doubt
        that implementing it with lists would be considerably faster.
        """

        _buffer = None

        def __init__(self):
                self._buffer = u""

        def __str__(self):
                return self._buffer

        def __repr__(self):
                return self._buffer

        def __len__(self):
                return len(self._buffer)

        def __hash__(self):
                return hash(self._buffer)
        
        def clear(self):
                self._buffer = ""

        def append(self, string):
                self._buffer = self._buffer + string
