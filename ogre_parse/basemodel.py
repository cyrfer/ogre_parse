__author__ = 'cyrfer'

import array

# should be hooked up to a 'basereader.colorspec' instance
class Color(object):
    def __init__(self, tokens=None):
        self.vector = array.array('f', [0, 0, 0, 1])

        if tokens and len(tokens)>0:
            for index in range(min(len(self.vector), len(tokens[0]))):
                self.vector[index] = tokens[0][index]

            # print('self.vector = %s' % self.vector)

    def __str__(self):
        return 'Color(%.2f, %.2f, %.2f, %.2f)' % (self.vector[0], self.vector[1], self.vector[2], self.vector[3])

    __repr__ = __str__

    def __getitem__(self, item):
        return self.vector.__getitem__(item)
