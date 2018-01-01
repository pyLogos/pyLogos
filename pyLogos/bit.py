'''    
pyLogos is inspired by MyHDL but loosely modeled after VHDL
    
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

from util import showwarning


class Bit(object):
    ''' 
        the basis of all logic
        it has three values: 0, 1 or 'Z'
    '''

    # using __slots__ to keep the size of the object as small as possible
    __slots__ = ('value', 'tristate', '_warningcount')

    def __init__(self, value=None, tristate=None):
        '''
            value: 0, 1 or 'Z', if None defaults to 0
            tristate: in the case of a physical (FPGA) pin, reading back a tristated pin
                      either returns a high or a low, when pull-up or pull-down resistors are specified
                      if no pull-up or pull-down is implemented we don't actually know what to do;
                      so we are going to infer a 0, but in simulation will issue a warning (once)
                      ('PullUp', PullDown', None)
        '''
        self.value = value if value is not None else 0
        self.tristate = tristate
        self._warningcount = 0

    @property
    def nbits(self):
        return 1

    # helper function(s)
    def _assess(self):
        if self.value == 'Z':
            if self.tristate is not None:
                return 1 if self.tristate == 'PullUp' else 0
            else:
                # echo a warning (in blue) only once
                if self._warningcount == 0:
                    showwarning('{} without pull-up or pull-down will assume \'0\''.format(repr(self)))
                self._warningcount += 1
                # then assume a pull-down
                return 0
        else:
            return self.value

    def _bool(self, other):
        return 0 if other == 0 else 1

    # representation
    def __str__(self):
        return '{}'.format(self._assess())

    def __repr__(self):
        return 'Bit: {}{}'.format(self.value, '' if self.tristate is None else ' {}'.format(self.tristate))

    def __len__(self):
        return 1

    # operations
    # return 0 or 1
    def __neg__(self):
        return 0 if self._assess() else 1

    def __invert__(self):
        return 0 if self._assess() else 1

    def __bool__(self):
        return self._assess() == 1

    def __int__(self):
        return int(self._assess())

    def __float__(self):
        return float(self._assess())

    def __and__(self, other):
        if isinstance(other, Bit):
            return self._assess() and other._assess()
        else:
            return self._assess() and self._bool(other)

    def __or__(self, other):
        if isinstance(other, Bit):
            return self._assess() or other._assess()
        else:
            return self._assess() or self._bool(other)

    def __rand__(self, other):
        return self._bool(other) and self._assess()

    def __ror__(self, other):
        return self._bool(other) or self._assess()

    def __xor__(self, other):
        if isinstance(other, Bit):
            return self._assess() ^ other._assess()
        else:
            return self._assess() ^ self._bool(other)

    def __rxor__(self, other):
        return self._bool(other) ^ self._assess()

    # comparisons
    # deliver True or False
    def __eq__(self, other):
        if isinstance(other, Bit):
            return self._assess() == other._assess()
        else:
            return self._assess() == other

    def __ne__(self, other):
        if isinstance(other, Bit):
            return self._assess() != other._assess()
        else:
            return self._assess() != other


if __name__ == '__main__':
    a = Bit()
    b = Bit(1)
    tu = Bit('Z', tristate='PullUp')
    td = Bit('Z', tristate='PullDown')
    tn = Bit('Z', tristate=None)

    print(' a:', repr(a))
    print(' b:', repr(b))
    print('tu:', repr(tu), '->', tu)
    print('td:', repr(td), '->', td)
    print('tn:', repr(tn), '->', tn)

    print('-a:', -a)
    print('~b:', ~b)

    print('a or tu:', a or tu)
    print('a | tu:', a | tu)
    print('td and b:', td and b)

    print('a == tu:', a == tu)
    print('b == td:', b == td)
    print('b == tn:', b == tn)
    print('a == 0:', a == 0)
    print('tu == 1:', tu == 1)
    print('tu ^ a:', tu ^ a)
    print('tu ^ b:', tu ^ b)
    print('tu ^ 0:', tu ^ 0)
    print('tu ^ 3:', tu ^ 3)

    print(tn._warningcount)
