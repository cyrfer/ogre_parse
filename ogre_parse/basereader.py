__author__ = 'cyrfer'


from pyparsing import Optional, Word, Literal, Keyword, Forward, alphas, nums, alphanums, \
    Group, ZeroOrMore, OneOrMore, oneOf, delimitedList, cStyleComment, restOfLine, LineEnd, \
    cppStyleComment, Combine, Dict, dictOf


def cvtInt(s, l, toks):
    return toks[0]

def cvtReal(s, l, toks):
    return toks[0]

def printAll(s, l, toks):
    print('-----------')
    print(toks)
    print('-----------')


# convenient definitions
# TODO: find a way that does not pollute the global namespace
EOL = LineEnd().suppress()
ident = Word( alphas+"_", alphanums+"_$@#." )
lbrace = Literal("{").suppress()
rbrace = Literal("}").suppress()

integer = Word(nums).setName('-integer-')
integer.setParseAction(cvtInt)

real = Combine(Optional(oneOf('+ -')) + Word(nums) + '.' + Optional(Word(nums))).setName('-real-')
real.setParseAction(cvtReal)

propVal = real | integer | ident
propList = Group(OneOrMore(~EOL + propVal))
# propList.setParseAction(printAll)

# # convenient definitions
# # TODO: find a way that does not pollute the global namespace
# EOL = LineEnd().setName('-EOL-')
# ident = Word( alphas+"_", alphanums+"_$@#." ).setName('-identifier-')
# lbrace = Literal("{").suppress()
# rbrace = Literal("}").suppress()
# integer = Word(nums).setName('-integer-')
# real = Combine(Optional(oneOf('+ -')) + Word(nums) + '.' + Optional(Word(nums))).setName('-real-')
# propVal = real | integer | ident
# propList = Group(OneOrMore(~EOL + propVal))


# base class for all parsers
class ReadBase(object):
    # all derived classes will provide the grammar object
    def __init__(self, grammar):
        self.grammar_ = grammar
        self.debug_flag_ = False
        self.grammar_.setDebug(True)

    def getGrammar(self):
        return self.grammar_

    def parseString(self, txt):

        if self.debug_flag_:
            print('parsing: [[\n' + txt + '\n]]\n')

        result = self.grammar_.parseString(txt)

        if self.debug_flag_:
            print('result = %s' % result )

        return result
