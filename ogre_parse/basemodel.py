__author__ = 'cyrfer'

import array
import math


def float_eq(a, b, epsilon=1e-7):
    # print('float_eq: type(a)=%s, type(b)=%s' % (type(a), type(b)))
    # print('float_eq(%s, %s)' % (a,b))
    diff_val = math.fabs(a - b)
    # print('float_eq: diff_val = %s' % diff_val)
    return  diff_val < epsilon


# should be hooked up to a 'basereader.colorspec' instance
class Color(object):
    def __init__(self, tokens=None, vals=None):
        self.vector = array.array('f', [0, 0, 0, 1])

        if vals:
            for i in range(min(4,len(vals))):
                self.vector[i] = vals[i]

        if tokens and len(tokens) > 0:
            for index in range(min(len(self.vector), len(tokens[0]))):
                self.vector[index] = tokens[0][index]

            # print('self.vector = %s' % self.vector)

    def __str__(self):
        fmt = '{0:.6f}'
        rep = fmt.format(self.vector[0]).rstrip('0').rstrip('.')
        rep += ' ' + fmt.format(self.vector[1]).rstrip('0').rstrip('.')
        rep += ' ' + fmt.format(self.vector[2]).rstrip('0').rstrip('.')
        rep += ' ' + fmt.format(self.vector[3]).rstrip('0').rstrip('.')

        return rep

    __repr__ = __str__

    def __getitem__(self, item):
        return self.vector.__getitem__(item)

    def __setitem__(self, key, value):
        return self.vector.__setitem__(key, value)

    def __eq__(self, other):
        if not isinstance(other, Color):
            return False

        if not other:
            # print('ogre_parse.basemodel.Color: why are we comparing with _%s_?' % other)
            return False

        if len(other)<4:
            # print('ogre_parse.basemodel.Color: len(other)=%s' % len(other))
            return False

        res = self.vector[0] == other[0] \
            and self.vector[1] == other[1] \
            and self.vector[2] == other[2] \
            and self.vector[3] == other[3]

        return res

    def __len__(self):
        return 4

