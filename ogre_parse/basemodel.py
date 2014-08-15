__author__ = 'cyrfer'

import array


# should be hooked up to a 'basereader.colorspec' instance
class Color(object):
    def __init__(self, tokens=None):
        self.vector = array.array('f', [0, 0, 0, 1])

        if tokens and len(tokens) > 0:
            for index in range(min(len(self.vector), len(tokens[0]))):
                self.vector[index] = tokens[0][index]

            # print('self.vector = %s' % self.vector)

    def __str__(self):
        rep = 'Color(%.2f, %.2f, %.2f, %.2f)' % (self.vector[0], self.vector[1], self.vector[2], self.vector[3])
        return rep

    __repr__ = __str__

    def __getitem__(self, item):
        # print('Color requesting item = %s, which has value = %s' % (item, self.vector.__getitem__(item)))
        return self.vector.__getitem__(item)

    def __setitem__(self, key, value):
        return self.vector.__setitem__(key, value)

    def __eq__(self, other):
        if not other:
            print('ogre_parse.basemodel.Color: why are we comparing with _%s_?' % other)
            return False

        if len(other)<4:
            print('ogre_parse.basemodel.Color: len(other)=%s' % len(other))
            return False

        res = self.vector[0] == other[0] \
            and self.vector[1] == other[1] \
            and self.vector[2] == other[2] \
            and self.vector[3] == other[3]

        return res

    def __len__(self):
        return 4

