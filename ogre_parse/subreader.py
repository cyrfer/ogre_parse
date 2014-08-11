__author__ = 'cyrfer'

# epic pyparsing help provided by Paul McGuire
# http://pyparsing.wikispaces.com/share/view/68890534


from ogre_parse.basereader import *
from ogre_parse.submodel import *

class ReadTextureUnit(ReadBase):
    def __init__(self):
        # TODO: need to separate the required member options
        textureResourceDecl = oneOf('texture anim_texture cubic_texture')('resource_type')

        texPropList = Group(identspec('name') + \
                      Optional( oneOf('1d 2d 3d cubic') )('type') + \
                      Optional(integer)('numMipMaps') + \
                      Optional(Literal('alpha'))('alpha') + \
                      Optional(oneOf(imageFormats)) + \
                      Optional(Literal('gamma')))
        textureResource = Group( textureResourceDecl + texPropList('resource_properties') )('required')

        # the optional members
        texturePropNameList = '''
        texture_alias
        tex_coord_set tex_address_mode tex_border_colour
        filtering
        '''
        texturePropName = oneOf( texturePropNameList )

        # --- define the parser
        textureDecl = Keyword('texture_unit').suppress() + Optional(ident)('name') + \
                        lbrace + \
                            (textureResource & dictOf(texturePropName, propList)('properties')) + \
                        rbrace

        texture_ = Group(textureDecl).setParseAction(MTextureUnit)

        super(ReadTextureUnit, self).__init__(texture_('texture_unit'))


class ReadShaderReference(ReadBase):
    def __init__(self):
        # --- define the shader_ref parser
        # shaderRefPropName = oneOf('param_indexed param_indexed_auto param_named param_named_auto shared_params_ref')

        param_named_auto_spec = Keyword('param_named_auto').suppress() + ident

        shaderRefDecl = oneOf('vertex_program_ref fragment_program_ref')('stage') + ident('resource_name') + \
                            lbrace + \
                                dictOf( param_named_auto_spec, propList )('param_named_auto') + \
                            rbrace
                                # (dictOf(param_named_auto, propList('system_params'))('param_named_auto')) + \
        shader_ref_ = Group(shaderRefDecl)
        shader_ref_.setParseAction(MShaderRef)

        super(ReadShaderReference, self).__init__(shader_ref_('shader_ref'))


# successful parsing produces a subreader.MPass in parsed.mpass
class ReadPass(ReadBase):
    def __init__(self):

        # self.texture_unit_ = ReadTextureUnit()
        # self.shader_ref_ = ReadShaderReference()
        #
        # # --- define the pass parser
        # passPropNameList = '''
        # ambient diffuse specular emissive
        # scene_blend separate_scene_blend scene_blend_op separate_scene_blend_op
        # depth_check depth_write depth_func depth_bias iteration_depth_bias
        # alpha_rejection alpha_to_coverage
        # light_scissor light_clip_planes
        # illumination_stage transparent_sorting normalize_normals
        # cull_hardware cull_software
        # lighting shading
        # polygon_mode polygon_mode_overrideable
        # fog_override
        # colour_write
        # max_lights start_light iteration
        # point_size point_sprites point_size_attenuation point_size_min point_size_max
        # '''
        # passPropName = oneOf(passPropNameList)
        # passPropName.setName('-Pass Prop Name-')
        # passProp = Group(passPropName + propList)
        # passProp.setName('-Pass Prop-')
        # # passMember = passProp | self.texture_unit_.getGrammar() | self.shader_ref_.getGrammar()
        # passDecl = Keyword('pass').suppress() + Optional(ident).suppress() + \
        #                 lbrace + \
        #                     Dict( passProp ) + \
        #                 rbrace
        #                     # ZeroOrMore( self.texture_unit_.getGrammar() | self.shader_ref_.getGrammar() ) + \
        #                     # ZeroOrMore(passMember) + \
        # self.pass_ = Group(passDecl)
        # self.pass_.setName('-Pass-')
        # self.pass_.setResultsName('pass')
        #
        # # self.pass_.setParseAction(printAll)

        # super(ReadPass, self).__init__(self.pass_)


        # -------------- NEW STUFF SINCE PAUL HELPED ------------ #
        # define named parsers
        color_ambient = Group(Keyword('ambient') + colorspec)('ambient')
        color_diffuse = Group(Keyword('diffuse') + colorspec)('diffuse')
        color_emissive = Group(Keyword('emissive') + colorspec)('emissive')

        specularspec = (color3spec('specular') + realspec('shininess')) ^ (color4spec('specular') + realspec('shininess'))
        color_specular = Group(Keyword('specular') + specularspec)('specular')

        tuspec = ReadTextureUnit().getGrammar()

        passBody = Group( Optional(color_ambient) + \
                          Optional(color_diffuse) + \
                          Optional(color_specular) + \
                          Optional(color_emissive) + \
                          ZeroOrMore(tuspec)('texture_units')
                        )('body')

        # total parser
        parser = Group( Keyword('pass')('type_value') + Optional(identspec('name')) + LBRACE + passBody + RBRACE)('mpass')
        parser.setParseAction(MPass)
        super(ReadPass, self).__init__(parser)
        # -------------- END NEW STUFF SINCE PAUL HELPED ------------ #



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

