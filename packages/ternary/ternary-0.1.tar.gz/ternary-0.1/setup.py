from setuptools import setup, find_packages

setup(
    name         = 'ternary',
    version      = '0.1',
    author       = 'Wijnand Modderman',
    author_email = 'maze@pyth0n.org',
    description  = ('Ternary operation implementation.'),
    long_description = '''
==================================
 Ternary operation implementation
==================================

This is a simple hack using the slice operation to mimic C-style
ternary operation::

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

Usage
=====

Using the slice operation::

    >>> value = ternary[condition:true_result:false_result]

''',
    license      = 'MIT',
    keywords     = 'ternary operation',
    packages     = {'': 'ternary.py'},
)

