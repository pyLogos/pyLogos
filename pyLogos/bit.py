'''    
pyLogos is inspired by MyHDL (see README) but loosely modeled after VHDL
    
    This file is part of the pyLogos library, a Python package for using
    Python as a Hardware Description Language.
    
    Copyright (C) 2017 Josy Boelen
    
    The pyLogos library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public License as
    published by the Free Software Foundation; either version 3.0 of the
    License, or (at your option) any later version.
    
    This library is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.
    
    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
    
Created on Dec 15, 2017

@author: josy
'''


class Bit(object):
    ''' 
        the basis of all logic
        it has only two values: 0 or 1
    '''

    # using __slots__ to keep the size of the object as small as possible
    # because we will have a lot of them
    __slots__ = ('_value')

    def __init__(self, value=None):
        '''
            value: 0 or 1, if None defaults to 0
        '''
        assert value in (None, 0, 1), 'A \'Bit\' must be either (0, 1, None)'
        self._value = value if value is not None else 0

    @property
    def nbits(self):
        return 1

    def _bool(self, other):
        return 0 if other == 0 else 1

    # representation
    def __str__(self):
        return '{}'.format(self._value)

    def __repr__(self):
        return 'Bit: {}'.format(self._value)

    def __len__(self):
        return 1

    # operations
    # return 0 or 1
    def __neg__(self):
        return 0 if self._value else 1

    def __invert__(self):
        return 0 if self._value else 1

    def __bool__(self):
        return self._value == 1

    def __int__(self):
        return int(self._value)

    def __float__(self):
        return float(self._value)

    def __and__(self, other):
        if isinstance(other, Bit):
            return self._value and other._value
        else:
            return self._value and self._bool(other)

    def __or__(self, other):
        if isinstance(other, Bit):
            return self._value or other._value
        else:
            return self._value or self._bool(other)

    def __rand__(self, other):
        return self._bool(other) and self._value

    def __ror__(self, other):
        return self._bool(other) or self._value

    def __xor__(self, other):
        if isinstance(other, Bit):
            return self._value ^ other._value
        else:
            return self._value ^ self._bool(other)

    def __rxor__(self, other):
        return self._bool(other) ^ self._value

    # comparisons
    # deliver True or False
    def __eq__(self, other):
        if isinstance(other, Bit):
            return self._value == other._value
        else:
            return self._value == other

    def __ne__(self, other):
        if isinstance(other, Bit):
            return self._value != other._value
        else:
            return self._value != other


if __name__ == '__main__':
    a = Bit()
    b = Bit(1)

    print(' a:', repr(a))
    print(' b:', repr(b))

    print('-a:', -a)
    print('~b:', ~b)

    print('a or b:', a or b)
    print('a | tbu:', a | b)
    print('a and b:', a and b)

    print('a == b:', a == b)
    print('a == 0:', a == 0)
    print('b == 1:', b == 1)
    print('b ^ a:', b ^ a)
    print('a ^ b:', a ^ b)
    print('b ^ 0:', b ^ 0)
    print('b ^ 3:', b ^ 3)

