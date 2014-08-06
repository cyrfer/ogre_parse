__author__ = 'cyrfer'

from ogre_parse.basereader import *


class ReadTextureUnit(ReadBase):
    def __init__(self):
        # --- define the texture parser
        texturePropName = oneOf("texture_alias texture anim_texture cubic_texture \
                                tex_coord_set tex_address_mode tex_border_colour filtering")
        # textureProp = texturePropName + OneOrMore(~texturePropName + ~EOL + Word(alphanums+'.'))
        texturePropName.setName('-Texture Prop Name-')
        textureProp = Group(texturePropName + propList)
        textureProp.setName('-Texture Prop-')
        textureDecl = Keyword('texture_unit') + Optional(ident).suppress() + \
                        lbrace + \
                            ZeroOrMore( textureProp ) + \
                        rbrace
        self.texture_ = Group(textureDecl)
        self.texture_.setName('-TextureUnit-')
        self.texture_.setResultsName('texture_unit')

        super(ReadTextureUnit, self).__init__(self.texture_)


class ReadShaderReference(ReadBase):
    def __init__(self):
        # --- define the shader_ref parser
        shaderRefPropName = oneOf('param_indexed param_indexed_auto param_named param_named_auto shared_params_ref')
        shaderRefPropName.setName('-Shader Ref Prop Name-')
        shaderRefProp = Group(shaderRefPropName + propList)
        shaderRefProp.setName('-Shader Ref Prop-')
                                # Group(ZeroOrMore(shaderRefProp)) + \
        shaderRefDecl = oneOf('vertex_program_ref fragment_program_ref') + ident + \
                            lbrace + \
                            rbrace
        self.shader_ref_ = Group(shaderRefDecl)
        self.shader_ref_.setName('-Shader Ref-')
        self.shader_ref_.setResultsName('shader_ref')

        super(ReadShaderReference, self).__init__(self.shader_ref_)


class ReadPass(ReadBase):
    def __init__(self):

        self.texture_unit_ = ReadTextureUnit()
        self.shader_ref_ = ReadShaderReference()

        # --- define the pass parser
        passPropName = oneOf('ambient diffuse specular emissive')
        passPropName.setName('-Pass Prop Name-')
        passProp = Group(passPropName + propList)
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


class ReadTechnique(ReadBase):
    def __init__(self):

        self.pass_ = ReadPass()

        # --- define the technique parser
        techPropName = oneOf('scheme lod_index shadow_caster_material shadow_receiver_material gpu_vendor_rule gpu_device_rule')
        techPropName.setName('-Technique Property Name-')
        techProp = Group(techPropName + propList)
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

