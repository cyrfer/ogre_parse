__author__ = 'cyrfer'

# base class for all parsers
class ReadBase(object):
    # all derived classes will provide the grammar object
    def __init__(self, grammar):
        self.grammar_ = grammar
        self.debug_flag_ = False
        self.grammar_.setDebug(False)

    def getGrammar(self):
        return self.grammar_

    def parseString(self, txt):

        if self.debug_flag_:
            print('parsing: [[\n' + txt + '\n]]\n')

        result = self.grammar_.parseString(txt)

        if self.debug_flag_:
            print('result = %s' % result )

        return result
