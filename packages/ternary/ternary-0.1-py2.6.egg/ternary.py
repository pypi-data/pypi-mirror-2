class Ternary(object):
    '''
    Ternary-ish emulation, it looks like C-style ternary operation::

        x = a ? b : c

    In Python we would write::

        >>> x = a and b or c

    Or (rather than above, this is safe for returning Falsy values for b)::

        >>> x = (a and [b] or [c])[0]

    Or::

        >>> x = b if a else c

    Or::

        >>> x = lambda i: (b, c)[not a]

    Or::

        >>> if a:
        ...     x = b
        ... else:
        ...     x = c

    Now we can also write::

        >>> x = ternary[a:b:c]
    '''
    __getitem__ = lambda s, sl: (sl.start and sl.stop, not sl.start and sl.step)[not sl.start]

# Actual "operation", we can only work with an instance
ternary = Ternary()

