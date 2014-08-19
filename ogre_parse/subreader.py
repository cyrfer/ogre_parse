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
        # define named parsers
        color_ambient = Group(Keyword('ambient').suppress() + colorspec)('ambient')
        color_diffuse = Group(Keyword('diffuse').suppress() + colorspec)('diffuse')
        color_emissive = Group(Keyword('emissive').suppress() + colorspec)('emissive')

        specular_spec = Group(colorspec('color') + real('shininess'))
        color_specular = Group(Keyword('specular').suppress() + specular_spec)('specular')

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
        depth_bias = Group(Keyword('depth_bias').suppress() + real('constant') + Optional(real('slopescale')))('depth_bias')
        iter_depth_bias = Group(Keyword('iteration_depth_bias').suppress() + real('bias'))('iteration_depth_bias')

        # alpha stuff
        alpha_rejection_func = depth_func_val_spec('function')
        alpha_rejection = Group(Keyword('alpha_rejection').suppress() + alpha_rejection_func + real('threshold'))('alpha_rejection')
        alpha_to_coverage = Group(Keyword('alpha_to_coverage').suppress() + onoff_val_spec)('alpha_to_coverage')

        # light_scissor
        light_scissor = Group(Keyword('light_scissor').suppress() + onoff_val_spec)('light_scissor')
        light_clip_planes = Group(Keyword('light_clip_planes').suppress() + onoff_val_spec)('light_clip_planes')

        # other
        illum_stage_val = oneOf('ambient per_light decal')
        illumination_stage = Group(Keyword('illumination_stage').suppress() + illum_stage_val)('illumination_stage')
        onoffforce_val_spec = oneOf('on off force')
        transparent_sorting = Group(Keyword('transparent_sorting').suppress() + onoffforce_val_spec)('transparent_sorting')
        normalise_normals = Group(Keyword('normalise_normals').suppress() + onoff_val_spec)('normalise_normals')

        # cull
        cull_hardware = Group(Keyword('cull_hardware').suppress() + oneOf('clockwise anticlockwise none'))('cull_hardware')
        cull_software = Group(Keyword('cull_software').suppress() + oneOf('back front none'))('cull_software')

        # other
        lighting = Group(Keyword('lighting').suppress() + onoff_val_spec)('lighting')
        shading = Group(Keyword('shading').suppress() + oneOf('flat gouraud phong'))('shading')
        polygon_mode = Group(Keyword('polygon_mode').suppress() + oneOf('solid wireframe points'))('polygon_mode')
        polygon_mode_overrideable = Group(Keyword('polygon_mode_overrideable').suppress() + truefalse_spec)('polygon_mode_overrideable')
        fog_override_type = oneOf('none linear exp exp2')

        # must define number spec here because
        # something is wrong with the specs for number types at this point (real, integer)
        # and they are returning a number and not a string.
        fog_int = Word(nums)
        fog_real = Regex(r"\d+\.\d*")
        fog_num = fog_int ^ fog_real

        fog_override_colour = fog_num + fog_num + fog_num
        fog_override_args = fog_override_type('type') + fog_override_colour('colour') + fog_num('density') + fog_num('start') + fog_num('end')
        fog_override = Group(Keyword('fog_override').suppress() + truefalse_spec('enabled') + Optional(fog_override_args))('fog_override')

        colour_write = Group(Keyword('colour_write').suppress() + onoff_val_spec)('colour_write')

        start_light = Group(Keyword('start_light').suppress() + integer)('start_light')
        max_lights = Group(Keyword('max_lights').suppress() + integer)('max_lights')

        light_type_spec = oneOf('point directional spot')

        iteration_format1 = oneOf('once once_per_light') + Optional(light_type_spec)
        iteration_format2 = integerspec + Optional(Keyword('per_light') + light_type_spec)
        iteration_format3 = integerspec + Optional(Keyword('per_n_lights') + integerspec + Optional(light_type_spec))
        iteration_args = (iteration_format1 ^ iteration_format2 ^ iteration_format3)
        iteration = Group(Keyword('iteration').suppress() + iteration_args)('iteration')

        point_size = Group(Keyword('point_size').suppress() + real)('point_size')
        point_sprites = Group(Keyword('point_sprites').suppress() + onoff_val_spec)('point_sprites')
        attenuation_spec = oneOf('constant linear quadratic')
        point_size_attenuation = Group(Keyword('point_size_attenuation').suppress() + onoff_val_spec('enabled') + Optional(attenuation_spec)('model'))('point_size_attenuation')
        point_size_min = Group(Keyword('point_size_min').suppress() + real)('point_size_min')
        point_size_max = Group(Keyword('point_size_max').suppress() + real)('point_size_max')


        tu = ReadTextureUnit()
        shader = ReadShaderReference()

        passBody = ( \
                     # color
                     Optional(color_ambient) + \
                     Optional(color_diffuse) + \
                     Optional(color_emissive) + \
                     Optional(color_specular) + \

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

                     # alpha
                     Optional(alpha_rejection) + \
                     Optional(alpha_to_coverage) + \

                     # light scissor
                     Optional(light_scissor) + \
                     Optional(light_clip_planes) + \

                     # other
                     Optional(illumination_stage) + \
                     Optional(transparent_sorting) + \
                     Optional(normalise_normals) + \

                     # cull
                     Optional(cull_hardware) + \
                     Optional(cull_software) + \

                     # lighting
                     Optional(lighting) + \
                     Optional(shading) + \

                     # polygon
                     Optional(polygon_mode) + \
                     Optional(polygon_mode_overrideable) + \

                     # other
                     Optional(fog_override) + \
                     Optional(colour_write) + \
                     Optional(start_light) + \
                     Optional(max_lights) + \
                     Optional(iteration) + \

                     # point
                     Optional(point_size) + \
                     Optional(point_sprites) + \
                     Optional(point_size_attenuation) + \
                     Optional(point_size_min) + \
                     Optional(point_size_max) + \

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

        pass_ = ReadPass()

        # --- define the technique parser
        scheme = Group(Keyword('scheme').suppress() + identspec)('scheme')
        lod_index = Group(Keyword('lod_index').suppress() + integer)('lod_index')
        shadow_caster_material = Group(Keyword('shadow_caster_material').suppress() + identspec)('shadow_caster_material')
        shadow_receiver_material = Group(Keyword('shadow_receiver_material').suppress() + identspec)('shadow_receiver_material')

        inex = oneOf('include exclude')
        gpu_vendor_rule = Group(Keyword('gpu_vendor_rule').suppress() + inex + identspec)('gpu_vendor_rule')
        gpu_device_rule = Group(Keyword('gpu_device_rule').suppress() + inex + propList)('gpu_device_rule')

        techDecl = Keyword('technique').suppress() + Optional(ident)('name') + \
                        lbrace + \
                            Optional( scheme ) + \
                            Optional( lod_index ) + \
                            Optional( shadow_caster_material ) + \
                            Optional( shadow_receiver_material ) + \
                            ZeroOrMore( gpu_vendor_rule )('gpu_vendor_rules') + \
                            ZeroOrMore( gpu_device_rule )('gpu_device_rules') + \
                            OneOrMore( pass_.getGrammar() )('passes') + \
                        rbrace
        technique_ = Group(techDecl)
        technique_.setParseAction(MTechnique)

        super(ReadTechnique, self).__init__(technique_('technique'))

