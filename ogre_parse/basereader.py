__author__ = 'cyrfer'


# from pyparsing import Optional, Word, Literal, Keyword, Forward, alphas, nums, alphanums, \
#     Group, ZeroOrMore, OneOrMore, oneOf, delimitedList, cStyleComment, restOfLine, LineEnd, \
#     cppStyleComment, Combine, Dict, dictOf, Regex, Suppress

from pyparsing import *

# import ogre_parse.model
import ogre_parse.basemodel

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

real = Regex(r"\d+\.\d*") #Combine(Optional(oneOf('+ -')) + Word(nums) + '.' + Optional(Word(nums))).setName('-real-')
real.setParseAction(cvtReal)

propVal = real | integer | ident
propList = Group(OneOrMore(~EOL + propVal))
# propList.setParseAction(printAll)


# reusable definitions
LBRACE, RBRACE = map(Suppress,'{}')
EOL = LineEnd().suppress()

# another option for floating point parsing:
# http://pyparsing.wikispaces.com/share/view/33656348
realspec = Regex(r"\d+\.\d*").setParseAction(lambda t: float(t[0]))

# colorspec = Group(~EOL + OneOrMore(realspec))('vector').setParseAction(Color)
color3spec = Group(realspec('r') + realspec('g') + realspec('b')).setParseAction(ogre_parse.basemodel.Color)
color4spec = Group(realspec('r') + realspec('g') + realspec('b') + realspec('a')).setParseAction(ogre_parse.basemodel.Color)
colorspec = ( color3spec ^ color4spec )('args')
identspec = Word( alphas+"_", alphanums+"_$@#." )

# on 8/8/2014, taken from:
# http://www.ogre3d.org/docs/manual/manual_17.html#texture
imageFormats = '''
    PF_L8 PF_L16 PF_A8 PF_A4L4 PF_BYTE_LA
    PF_R5G6B5 PF_B5G6R5 PF_R3G3B2 PF_A4R4G4B4 PF_A1R5G5B5
    PF_R8G8B8 PF_B8G8R8
    PF_A8R8G8B8 PF_A8B8G8R8 PF_B8G8R8A8 PF_R8G8B8A8
    PF_X8R8G8B8 PF_X8B8G8R8
    PF_A2R10G10B10 PF_A2B10G10R10
    PF_DXT1 PF_DXT2 PF_DXT3 PF_DXT4 PF_DXT5
    PF_FLOAT16_R PF_FLOAT16_RGB PF_FLOAT16_RGBA
    PF_FLOAT32_R PF_FLOAT32_RGB PF_FLOAT32_RGBA
    PF_SHORT_RGBA
    PF_FLOAT16_GR PF_FLOAT32_GR
    PF_DEPTH
    PF_SHORT_GR PF_SHORT_RGB
    PF_PVRTC_RGB2 PF_PVRTC_RGBA2 PF_PVRTC_RGB4 PF_PVRTC_RGBA4
    PF_R8 PF_RG8
'''

# base class for all parsers
class ReadBase(object):
    # all derived classes will provide the grammar object
    def __init__(self, grammar):
        self.grammar_ = grammar
        self.grammar_.ignore( cppStyleComment )
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
