__author__ = 'cyrfer'

import ogre_parse.basereader

from pyparsing import Optional, Word, Literal, Keyword, Forward, alphas, nums, alphanums, \
    Group, ZeroOrMore, OneOrMore, oneOf, delimitedList, cStyleComment, restOfLine, LineEnd, cppStyleComment

# convenient definitions
# TODO: find a way that does not pollute the global namespace
EOL = LineEnd().suppress()
ident = Word( alphas+"_", alphas+nums+"_$" )
lbrace = Literal("{").suppress()
rbrace = Literal("}").suppress()
prop_val_string = Word(alphanums+'_.')

class ReadTextureUnit(ogre_parse.basereader.ReadBase):
    def __init__(self):
        # --- define the texture parser
        texturePropName = oneOf("texture_alias texture anim_texture cubic_texture \
                                tex_coord_set tex_address_mode tex_border_colour filtering")
        # textureProp = texturePropName + OneOrMore(~texturePropName + ~EOL + Word(alphanums+'.'))
        texturePropName.setName('-Texture Prop Name-')
        textureProp = Group(texturePropName + Group(OneOrMore(~EOL + prop_val_string)))
        textureProp.setName('-Texture Prop-')
        textureDecl = Keyword('texture_unit') + Optional(ident).suppress() + \
                        lbrace + \
                            ZeroOrMore( textureProp ) + \
                        rbrace
        self.texture_ = Group(textureDecl)
        self.texture_.setName('-TextureUnit-')
        self.texture_.setResultsName('texture_unit')

        super(ReadTextureUnit, self).__init__(self.texture_)


class ReadShaderReference(ogre_parse.basereader.ReadBase):
    def __init__(self):
        # --- define the shader_ref parser
        shaderRefPropName = oneOf('param_indexed param_indexed_auto param_named param_named_auto shared_params_ref')
        shaderRefPropName.setName('-Shader Ref Prop Name-')
        shaderRefProp = Group(shaderRefPropName + Group(OneOrMore(~EOL + prop_val_string)))
        shaderRefProp.setName('-Shader Ref Prop-')
                                # Group(ZeroOrMore(shaderRefProp)) + \
        shaderRefDecl = oneOf('vertex_program_ref fragment_program_ref') + ident + \
                            lbrace + \
                            rbrace
        self.shader_ref_ = Group(shaderRefDecl)
        self.shader_ref_.setName('-Shader Ref-')
        self.shader_ref_.setResultsName('shader_ref')

        super(ReadShaderReference, self).__init__(self.shader_ref_)


class ReadPass(ogre_parse.basereader.ReadBase):
    def __init__(self):

        self.texture_unit_ = ReadTextureUnit()
        self.shader_ref_ = ReadShaderReference()

        # --- define the pass parser
        passPropName = oneOf('ambient diffuse specular emissive')
        passPropName.setName('-Pass Prop Name-')
        passProp = Group(passPropName + Group(OneOrMore(~EOL + prop_val_string)))
        passProp.setName('-Pass Prop-')
        passMember = passProp | self.texture_unit_.getGrammar() | self.shader_ref_.getGrammar()
        passDecl = Keyword('pass').suppress() + Optional(ident).suppress() + \
                        lbrace + \
                            ZeroOrMore(passMember) + \
                        rbrace
        self.pass_ = Group(passDecl)
        self.pass_.setName('-Pass-')
        self.pass_.setResultsName('pass')

        super(ReadPass, self).__init__(self.pass_)


class ReadTechnique(ogre_parse.basereader.ReadBase):
    def __init__(self):

        self.pass_ = ReadPass()

        # --- define the technique parser
        techPropName = oneOf('scheme lod_index shadow_caster_material shadow_receiver_material gpu_vendor_rule gpu_device_rule')
        techPropName.setName('-Technique Property Name-')
        techProp = Group(techPropName + Group(OneOrMore(~EOL + prop_val_string)))
        techProp.setName('-Technique Property-')
        techMember = self.pass_.getGrammar() | techProp
        techDecl = Keyword('technique').suppress() + Optional(ident).suppress() + \
                        lbrace + \
                            ZeroOrMore( techMember ) + \
                        rbrace
        self.technique_ = Group(techDecl)
        self.technique_.setName('-Technique-')
        self.technique_.setResultsName('technique')

        super(ReadTechnique, self).__init__(self.technique_)

