__author__ = 'cyrfer'

# This file defines 'readers' for the major classes of OGRE objects, including:
# - materials
# - shader declarations
# - compositors

# OGRE permits putting any of the major classes into any of the OGRE resource file types, including:
# - .material
# - .program
# - .compositor

# Because any script may define any of the definitions, a catch-all "script reader" is defined here.


import ogre_parse.basereader
import ogre_parse.subreader

# import pyparsing as pp
from pyparsing import Optional, Word, Literal, Keyword, Forward, alphas, nums, alphanums, \
    Group, ZeroOrMore, OneOrMore, oneOf, delimitedList, cStyleComment, restOfLine, LineEnd, cppStyleComment

import pprint

# convenient definitions
# TODO: find a way that does not pollute the global namespace
EOL = LineEnd().suppress()
ident = Word( alphas+"_", alphas+nums+"_$" )
lbrace = Literal("{").suppress()
rbrace = Literal("}").suppress()
prop_val_string = Word(alphanums+'_.')


# grammar to parse materials
class ReadMaterial(ogre_parse.basereader.ReadBase):
    def __init__(self):
        self.technique_ = ogre_parse.subreader.ReadTechnique()

        # --- define the material parser
        matPropName = oneOf('lod_strategy lod_values receive_shadows transparency_casts_shadows set_texture_alias')
        matProp = Group(matPropName  + Group(OneOrMore(~EOL + prop_val_string)))
        matMember = self.technique_.getGrammar() | matProp
        matDecl = Keyword('material').suppress() + Optional(ident).suppress() + \
                        lbrace + \
                            ZeroOrMore( matMember ) + \
                        rbrace
        self.material_ = matDecl
        self.material_.setName('-Material-')
        super(ReadMaterial, self).__init__(self.material_)


# grammar to parse shader declarations
class ReadShaderDeclaration(ogre_parse.basereader.ReadBase):
    def __init__(self):
        shaderDeclPropName = oneOf('source entry_point target delegate')
        shaderDeclProp = Group(shaderDeclPropName + OneOrMore(~EOL + prop_val_string))
        shaderType = oneOf('vertex_program geometry_program fragment_program')
        shaderName = ident
        shaderLang = oneOf('glsl hlsl cg asm')
        shaderDeclDecl = shaderType + shaderName + shaderLang + \
                            lbrace + \
                                ZeroOrMore(shaderDeclProp) + \
                            rbrace
                                # (shaderDeclProps_unified | shaderDeclProps_hlsl | shaderDeclProps_glsl | shaderDeclProps_cg | shaderDeclProps_asm)
        shader_declaration = Group(shaderDeclDecl)
        shader_declaration.setName('-Shader Declaration-')
        super(ReadShaderDeclaration, self).__init__(shader_declaration)


# grammar to parse compositors
class ReadCompositor(ogre_parse.basereader.ReadBase):
    def __init__(self):
        compTexture = Group(Keyword('texture') + OneOrMore(ident))
        compTargetPropName = oneOf('input only_initial visibility_mask load_bias material_scheme shadows pass')
        compTargetProp = Group(compTargetPropName)
        compTarget = Group(Keyword('target') + ident + lbrace + ZeroOrMore(compTargetProp) + rbrace)
        compOutput = Group(Keyword('target_output') + lbrace + ZeroOrMore(compTargetProp) + rbrace)
        compTech = Group(Keyword('technique').suppress() + \
                    lbrace + \
                        ZeroOrMore(compTexture) + \
                        ZeroOrMore(compTarget) + \
                        compOutput + \
                    rbrace)

        compDecl = Keyword('compositor').suppress() + ident + \
                    lbrace + \
                        OneOrMore(compTech) + \
                    rbrace

        compositor = Group(compDecl)
        super(ReadCompositor, self).__init__(compositor)


# grammar to parse anything in an ogre script (.material, .compositor, .program)
class ReadScript(ogre_parse.basereader.ReadBase):
    def __init__(self):
        self.material_ = ReadMaterial()
        self.shader_declaration_ = ReadShaderDeclaration()
        self.compositor_ = ReadCompositor()

        scriptDecl = ZeroOrMore( self.material_.getGrammar() | \
                                 self.shader_declaration_.getGrammar() | \
                                 self.compositor_.getGrammar() )

        scriptDecl.ignore(cppStyleComment)

        super(ReadScript, self).__init__(scriptDecl)

    def getGrammar(self):
        return self.grammar_

