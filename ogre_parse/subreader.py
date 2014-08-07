__author__ = 'cyrfer'

from ogre_parse.basereader import *
import ogre_parse.model


class ReadTextureUnit(ReadBase):
    def __init__(self):
        # --- define the texture parser
        textureResourceDecl = oneOf('texture anim_texture cubic_texture')
        textureResource = Group( textureResourceDecl + propList ).setResultsName('texture')

        texturePropNameList = '''
        texture_alias
        tex_coord_set tex_address_mode tex_border_colour
        filtering
        '''
        texturePropName = oneOf( texturePropNameList )
        texturePropName.setName('-Texture Prop Name-')
        # textureProp = Group(texturePropName + propList)
        # textureProp.setName('-Texture Prop-')
        textureDecl = Keyword('texture_unit').suppress() + Optional(ident).setResultsName('name') + \
                        lbrace + \
                            (textureResource  & dictOf(texturePropName, propList).setResultsName('properties')) + \
                        rbrace
                             # Dict( ZeroOrMore( textureProp ) )) + \
        self.texture_ = Group(textureDecl)
        self.texture_.setName('-TextureUnit-')
        # self.texture_.setResultsName('texture_unit')
        # self.texture_.setParseAction(printAll)

        super(ReadTextureUnit, self).__init__(self.texture_.setResultsName('texture_unit'))


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

        self.shader_ref_.setParseAction(printAll)

        super(ReadShaderReference, self).__init__(self.shader_ref_)


class ReadPass(ReadBase):
    def __init__(self):

        self.texture_unit_ = ReadTextureUnit()
        self.shader_ref_ = ReadShaderReference()

        # --- define the pass parser
        passPropNameList = '''
        ambient diffuse specular emissive
        scene_blend separate_scene_blend scene_blend_op separate_scene_blend_op
        depth_check depth_write depth_func depth_bias iteration_depth_bias
        alpha_rejection alpha_to_coverage
        light_scissor light_clip_planes
        illumination_stage transparent_sorting normalize_normals
        cull_hardware cull_software
        lighting shading
        polygon_mode polygon_mode_overrideable
        fog_override
        colour_write
        max_lights start_light iteration
        point_size point_sprites point_size_attenuation point_size_min point_size_max
        '''
        passPropName = oneOf(passPropNameList)
        passPropName.setName('-Pass Prop Name-')
        passProp = Group(passPropName + propList)
        passProp.setName('-Pass Prop-')
        # passMember = passProp | self.texture_unit_.getGrammar() | self.shader_ref_.getGrammar()
        passDecl = Keyword('pass').suppress() + Optional(ident).suppress() + \
                        lbrace + \
                            Dict( passProp ) + \
                        rbrace
                            # ZeroOrMore( self.texture_unit_.getGrammar() | self.shader_ref_.getGrammar() ) + \
                            # ZeroOrMore(passMember) + \
        self.pass_ = Group(passDecl)
        self.pass_.setName('-Pass-')
        self.pass_.setResultsName('pass')

        # self.pass_.setParseAction(printAll)

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

        self.technique_.setParseAction(printAll)

        super(ReadTechnique, self).__init__(self.technique_)

