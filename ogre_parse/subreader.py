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
# format documented here:
# http://www.ogre3d.org/docs/manual/manual_16.html#Passes
class ReadPass(ReadBase):
    def __init__(self):
        onoff_val_spec = oneOf('on off')

        # define named parsers
        color_ambient = Group(Keyword('ambient') + colorspec)('ambient')
        color_diffuse = Group(Keyword('diffuse') + colorspec)('diffuse')
        color_emissive = Group(Keyword('emissive') + colorspec)('emissive')

        specularspec = (color3spec('specular') + realspec('shininess')) ^ (color4spec('specular') + realspec('shininess'))
        color_specular = Group(Keyword('specular') + specularspec)('specular')

        # scene_blend
        # TODO: add action to turn short format into long format
        scene_blend_short = oneOf('add modulate colour_blend alpha_blend')
        scene_blend_long_spec = oneOf('one zero dest_colour src_colour one_minus_dest_colour one_minus_src_colour dest_alpha src_alpha one_minus_dest_alpha one_minus_src_alpha')
        scene_blend_long = scene_blend_long_spec + scene_blend_long_spec
        scene_blend = Group(Keyword('scene_blend').suppress() + (scene_blend_short | scene_blend_long))('scene_blend')

        # TODO: add action to turn short format into long format
        separate_blend_short = scene_blend_short + scene_blend_short
        separate_blend_long = scene_blend_long_spec + scene_blend_long_spec + scene_blend_long_spec + scene_blend_long_spec
        separate_scene_blend = Group(Keyword('separate_scene_blend').suppress() + (separate_blend_short | separate_blend_long))('separate_scene_blend')
        scene_blend_op_spec = oneOf('add subtract reverse_subtract min max')
        scene_blend_op = Group(Keyword('scene_blend_op').suppress() + scene_blend_op_spec)('scene_blend_op')
        separate_scene_blend_op = Group(Keyword('separate_scene_blend_op').suppress() + (scene_blend_op_spec+scene_blend_op_spec))('separate_scene_blend_op')

        # depth stuff
        depth_check = Group(Keyword('depth_check').suppress() + onoff_val_spec)('depth_check')
        depth_write = Group(Keyword('depth_write').suppress() + onoff_val_spec)('depth_write')
        depth_func_val_spec = oneOf('always_fail always_pass less less_equal equal not_equal greater_equal greater')
        depth_func = Group(Keyword('depth_func').suppress() + depth_func_val_spec)('depth_func')
        depth_bias = Group(Keyword('depth_bias').suppress() + realspec('constant') + Optional(realspec('slopescale')))('depth_bias')
        iter_depth_bias = Group(Keyword('iteration_depth_bias').suppress() + realspec('bias'))('iteration_depth_bias')

        tu = ReadTextureUnit()
        shader = ReadShaderReference()

        passBody = ( \
                     # color
                     Optional(color_ambient) + \
                     Optional(color_diffuse) + \
                     Optional(color_specular) + \
                     Optional(color_emissive) + \

                     # blend
                     Optional(scene_blend) + \
                     Optional(separate_scene_blend) + \
                     Optional(scene_blend_op) + \
                     Optional(separate_scene_blend_op) + \

                     # depth
                     Optional(depth_check) + \
                     Optional(depth_write) + \
                     Optional(depth_func) + \
                     Optional(depth_bias) + \
                     Optional(iter_depth_bias) + \

                     # texture
                     ZeroOrMore(tu.getGrammar())('texture_units') + \

                     # shaders
                     ZeroOrMore(shader.getGrammar())('shaders') \
                   )

        # total parser
        parser = Group( Keyword('pass').suppress() + Optional(identspec('name')) + LBRACE + passBody + RBRACE)('mpass')
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

