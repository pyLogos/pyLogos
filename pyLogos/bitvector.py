'''
Created on Dec 15, 2017

@author: josy
'''



from pyLogos.bit import Bit
from pyLogos.util import widthu


class BitVector(object):
    '''
        like the std_logic_vector in VHDL the BitVector is an array of Bits
        with shortcuts, i.e. 
    '''
    def __init__(self, widthspecifier, value=0):
        '''
            widthspecifier:
                positive int: defines an unsigned BitVector of width bits wide
                negative int: defines a signed BitVector of width bits wide
                tuple(min, max): min and max are used to define both signedness and width
                None: special case expecting the value to be a list of Bit
            value: initialisation value to use
                int
                str: a binary string with underscores allowed
                list or tuple of Bit
        '''
        if widthspecifier is None:
            assert isinstance(value, (list, tuple)), 'Expecting a list (or tuple) of Bit'
            assert isinstance(value[0], Bit), 'Elements of supplied list (tuple) must be of class Bit'
            self._nbits = len(value)
            # defaults to unsigned (for now)
            self.min = 0
            self.max = 2**self._nbits
            self.value = value
        else:                      
            if isinstance(widthspecifier, int):
                if widthspecifier > 0:
                    self._nbits = widthspecifier
                    self.min = 0
                    self.max = 2 ** widthspecifier
                if widthspecifier < 0:
                    self._nbits = -widthspecifier
                    self.min = -(2 ** (widthspecifier - 1))
                    self.max = 2 ** (widthspecifier - 1)

            elif isinstance(widthspecifier, float):
                raise NotImplementedError('BitVector: fixed not yet implemented')

            elif isinstance(widthspecifier, tuple):
                self.min = widthspecifier[0]
                self.max = widthspecifier[1]
                assert self.max > self.min, 'BitVector: max ({}) needs to be greater than min ({})'.format(self.max, self.min)
                if self.min >= 0:
                    self._nbits = widthu(self.max)
                elif self.max <= 0:
                    self._nbits = widthu(self.min) 
                else:
                    # min < 0
                    # max > 0
                    self._nbits = widthu(max(self.max, -self.min)) + 1

            else:
                # print a helpful message
                
                # then raise an exception
                raise ValueError('Unhandled Width Specifier {} for BitVector'.format(widthspecifier))
        
        self.value = value
            

    @property
    def nbits(self):
        return self._nbits

        
if __name__ == '__main__':
    pass
