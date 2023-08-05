# encoding=UTF-8
# Copyright © 2007, 2008, 2010 Jakub Wilk <jwilk@jwilk.net>
#
# This package is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# This package is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

from nose.tools import *

from djvu.sexpr import *

class IntExpressionTest:
    '''
    >>> x = Expression(3)
    >>> x
    Expression(3)

    >>> x is Expression(x)
    True

    >>> x.value
    3

    >>> str(x)
    '3'

    >>> repr(x) == repr(Expression.from_string(str(x)))
    True

    >>> int(x)
    3
    >>> long(x)
    3L

    >>> x == Expression(3)
    True
    >>> x == Expression(-3)
    False
    >>> hash(x) == x.value
    True
    >>> x == 3
    False

    >>> Expression(42L)
    Expression(42)

    >>> [Expression(i).value == i for i in (1 << 29 - 1, -1 << 29)]
    [True, True]
    >>> Expression(1 << 29)
    Traceback (most recent call last):
    ...
    ValueError: value not in range(-2 ** 29, 2 ** 29)
    >>> Expression((-1 << 29) - 1)
    Traceback (most recent call last):
    ...
    ValueError: value not in range(-2 ** 29, 2 ** 29)

    >>> Expression(1) and 42
    42
    >>> Expression(0) or 42
    42

    '''

def test_symbols():

    for name in 'eggs', u'ветчина':
        symbol = Symbol(name)
        assert_equal(type(symbol), Symbol)
        assert_equal(symbol, Symbol(name))
        assert symbol is Symbol(name)
        assert_equal(str(symbol), name.encode('UTF-8'))
        assert_equal(unicode(symbol), name)
        assert_not_equal(symbol, name)
        assert_not_equal(symbol, name.encode('UTF-8'))
        assert_equal(hash(symbol), hash(name.encode('UTF-8')))

class SymbolExpressionTest:
    '''
    >>> x = Expression(Symbol('eggs'))
    >>> x
    Expression(Symbol('eggs'))

    >>> x is Expression(x)
    True

    >>> x.value
    Symbol('eggs')

    >>> str(x)
    'eggs'

    >>> repr(x) == repr(Expression.from_string(str(x)))
    True

    >>> x == Expression(Symbol('eggs'))
    True
    >>> x == Expression('eggs')
    False
    >>> x == Symbol('eggs')
    False
    >>> hash(x) == hash('eggs')
    True
    '''

class StringExpressionTest:
    '''
    >>> x = Expression('eggs')
    >>> x
    Expression('eggs')

    >>> x is Expression(x)
    True

    >>> x.value
    'eggs'

    >>> str(x)
    '"eggs"'

    >>> repr(x) == repr(Expression.from_string(str(x)))
    True

    >>> x == Expression('eggs')
    True
    >>> x == Expression(Symbol('eggs'))
    False
    >>> x == 'eggs'
    False
    >>> hash(x) == hash('eggs')
    True
    '''

class UnicodeExpressionTest:
    r'''
    >>> x = Expression(u'eggs')
    >>> x
    Expression('eggs')
    >>> x is Expression(x)
    True

    >>> x = Expression(u'\u017c\xf3\u0142w')
    >>> x
    Expression('\xc5\xbc\xc3\xb3\xc5\x82w')
    '''

class ListExpressionTest:
    '''
    >>> x = Expression(())
    >>> x
    Expression(())

    >>> y = Expression(x)
    >>> x is y
    True

    >>> x.value
    ()

    >>> len(x)
    0

    >>> bool(x)
    False

    >>> list(x)
    []

    >>> x = Expression([[1, 2], 3, [4, 5, Symbol('baz')], ['quux']])
    >>> x
    Expression(((1, 2), 3, (4, 5, Symbol('baz')), ('quux',)))
    >>> y = Expression(x)
    >>> repr(x) == repr(y)
    True
    >>> x is y
    False

    >>> x.value
    ((1, 2), 3, (4, 5, Symbol('baz')), ('quux',))

    >>> str(x)
    '((1 2) 3 (4 5 baz) ("quux"))'

    >>> repr(x) == repr(Expression.from_string(str(x)))
    True

    >>> len(x)
    4

    >>> bool(x)
    True

    >>> tuple(x)
    (Expression((1, 2)), Expression(3), Expression((4, 5, Symbol('baz'))), Expression(('quux',)))

    >>> x[object()]
    Traceback (most recent call last):
    ...
    TypeError: key must be an integer or a slice

    >>> x[1]
    Expression(3)

    >>> x[-1][0]
    Expression('quux')

    >>> x[6]
    Traceback (most recent call last):
    ...
    IndexError: list index of out range
    >>> x[-6]
    Traceback (most recent call last):
    ...
    IndexError: list index of out range

    >>> x[:].value == x.value
    True

    >>> x[1:]
    Expression((3, (4, 5, Symbol('baz')), ('quux',)))
    >>> x[-2:]
    Expression(((4, 5, Symbol('baz')), ('quux',)))

    >>> x[-2:] = 4, 5, 6
    >>> x
    Expression(((1, 2), 3, 4, 5, 6))
    >>> x[0] = 2
    >>> x
    Expression((2, 3, 4, 5, 6))
    >>> x[:] = (1, 3, 5)
    >>> x
    Expression((1, 3, 5))
    >>> x[3:] = 7,
    >>> x
    Expression((1, 3, 5, 7))

    >>> x[object():]
    Traceback (most recent call last):
    ...
    NotImplementedError: only [n:] slices are supported
    >>> x[:2]
    Traceback (most recent call last):
    ...
    NotImplementedError: only [n:] slices are supported
    >>> x[object():] = []
    Traceback (most recent call last):
    ...
    NotImplementedError: only [n:] slices are supported
    >>> x[:2] = []
    Traceback (most recent call last):
    ...
    NotImplementedError: only [n:] slices are supported
    >>> x[:] = 0
    Traceback (most recent call last):
    ...
    TypeError: can only assign a list expression

    >>> x == Expression((1, 3, 5, 7))
    True
    >>> x == Expression((2, 4, 6))
    False
    >>> x == (1, 3, 5, 7)
    False
    >>> hash(x)
    Traceback (most recent call last):
    ...
    TypeError: unhashable type: 'ListExpression'

    '''

class ListExpressionCopyTest:

    '''
    >>> from copy import copy, deepcopy

    >>> x = Expression([1, [2], 3])
    >>> y = Expression(x)
    >>> x[1][0] = 0
    >>> x
    Expression((1, (0,), 3))
    >>> y
    Expression((1, (0,), 3))
    >>> x[1] = 0
    >>> x
    Expression((1, 0, 3))
    >>> y
    Expression((1, (0,), 3))

    >>> x = Expression([1, [2], 3])
    >>> y = copy(x)
    >>> x[1][0] = 0
    >>> x
    Expression((1, (0,), 3))
    >>> y
    Expression((1, (0,), 3))
    >>> x[1] = 0
    >>> x
    Expression((1, 0, 3))
    >>> y
    Expression((1, (0,), 3))


    >>> x = Expression([1, [2], 3])
    >>> y = deepcopy(x)
    >>> x[1][0] = 0
    >>> x
    Expression((1, (0,), 3))
    >>> y
    Expression((1, (2,), 3))
    >>> x[1] = 0
    >>> x
    Expression((1, 0, 3))
    >>> y
    Expression((1, (2,), 3))
    '''

class ExpressionParser:
    '''
    >>> Expression.from_string('(1')
    Traceback (most recent call last):
    ...
    ExpressionSyntaxError

    >>> Expression.from_stream(42)
    Traceback (most recent call last):
    ...
    ExpressionSyntaxError

    >>> from cStringIO import StringIO
    >>> fp = StringIO('(eggs) (ham)')
    >>> from djvu.sexpr import *
    >>> Expression.from_stream(fp)
    Expression((Symbol('eggs'),))
    >>> Expression.from_stream(fp)
    Expression((Symbol('ham'),))
    >>> Expression.from_stream(fp)
    Traceback (most recent call last):
    ...
    ExpressionSyntaxError

    >>> import tempfile
    >>> fp = tempfile.TemporaryFile()
    >>> type(fp)
    <type 'file'>
    >>> fp.write('(eggs) (ham)')
    >>> fp.seek(0)
    >>> Expression.from_file(f)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: type object 'Expression' has no attribute 'from_file'
    >>> Expression.from_stream(fp)
    Expression((Symbol('eggs'),))
    >>> Expression.from_stream(fp)
    Expression((Symbol('ham'),))
    >>> Expression.from_stream(fp)
    Traceback (most recent call last):
    ...
    ExpressionSyntaxError
    '''

class ExpressionWriter:

    '''
    >>> expr = Expression([Symbol('eggs'), Symbol('ham')])

    >>> expr.print_into(42)

    >>> from cStringIO import StringIO
    >>> fp = StringIO()
    >>> expr.print_into(fp)
    >>> fp.getvalue()
    '(eggs ham)'

    >>> import tempfile
    >>> fp = tempfile.TemporaryFile()
    >>> type(fp)
    <type 'file'>
    >>> expr.print_into(fp)
    >>> fp.seek(0)
    >>> fp.read()
    '(eggs ham)'
    '''

# vim:ts=4 sw=4 et
