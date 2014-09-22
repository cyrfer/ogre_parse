__author__ = 'jgrant'

import unittest

# same imports as client code
import ogre_parse.reader
import ogre_parse.subreader
import ogre_parse.basereader
import ogre_parse.basemodel
from ogre_parse.basemodel import *

import ogre_parse.basereader
import ogre_parse.basemodel

import pyparsing
from pyparsing import *
import math

def float_eq(a, b, epsilon=1e-7):
    # print('float_eq: type(a)=%s, type(b)=%s' % (type(a), type(b)))
    # print('float_eq(%s, %s)' % (a,b))
    diff_val = math.fabs(a - b)
    # print('float_eq: diff_val = %s' % diff_val)
    return  diff_val < epsilon


# --------------------------------------------- #

test_color_3 = '0.1 0.2 0.3'
test_color_4 = '0.1 0.2 0.3 0.4'

class TestColor(unittest.TestCase):
    def setUp(self):
        self.reader_ = ogre_parse.basereader.colorspec

    def test_color_constructor(self):
        c = ogre_parse.basemodel.Color([[1, 2, 3]])

        self.assertEqual(1, c[0])
        self.assertEqual(2, c[1])
        self.assertEqual(3, c[2])

        cc = ogre_parse.basemodel.Color(vals=[1, 2, 3])

        self.assertEqual(1, cc[0])
        self.assertEqual(2, cc[1])
        self.assertEqual(3, cc[2])

    def test_color_op_bracket(self):
        c = ogre_parse.basemodel.Color()

        c[0] = 0.5
        c[1] = 0.6
        c[2] = 0.7
        c[3] = 0.8

        self.assertTrue(float_eq(0.5, c[0]))
        self.assertTrue(float_eq(0.6, c[1]))
        self.assertTrue(float_eq(0.7, c[2]))
        self.assertTrue(float_eq(0.8, c[3]))

    def test_color_op_eq_ne(self):
        c = ogre_parse.basemodel.Color(vals=[1.0, 2.0, 3.0, 4.0])
        cc = ogre_parse.basemodel.Color(vals=[1.0, 2.0, 3.0, 4.0])
        rr = ogre_parse.basemodel.Color(vals=[5.0, 2.0, 3.0, 4.0])
        gg = ogre_parse.basemodel.Color(vals=[1.0, 1.0, 3.0, 4.0])

        self.assertTrue(c == cc)
        self.assertTrue(c != rr)
        self.assertTrue(c != gg)
        self.assertEqual(c, cc)


    def test_color_3(self):
        res = self.reader_.parseString(test_color_3)

        c = ogre_parse.basemodel.Color(vals=[0.1, 0.2, 0.3])
        # self.assertEqual(c, res[0])
        self.assertEqual(c, res.args)

    def test_color_4(self):
        res = self.reader_.parseString(test_color_4)

        c = ogre_parse.basemodel.Color(vals=[0.1, 0.2, 0.3, 0.4])
        # self.assertEqual(c, res[0])
        self.assertEqual(c, res.args)

# --------------------------------------------- #
test_ambient_3 = 'ambient 0.1 0.2 0.3'
test_diffuse_3 = 'diffuse 0.1 0.2 0.3'
test_emissive_3 = 'emissive 0.1 0.2 0.3'
test_specular_3 = 'specular 0.1 0.2 0.3 25.0'

test_ambient_4 = 'ambient 0.1 0.2 0.3 1.0'
test_diffuse_4 = 'diffuse 0.1 0.2 0.3 1.0'
test_emissive_4 = 'emissive 0.1 0.2 0.3 1.0'
test_specular_4 = 'specular 0.1 0.2 0.3 1.0 25.0'

class TestColorParsers(unittest.TestCase):
    def setUp(self):
        # define parsers
        self.ambient = Group(Keyword('ambient').suppress() + ogre_parse.basereader.colorspec)('ambient')
        self.diffuse = Group(Keyword('diffuse').suppress() + ogre_parse.basereader.colorspec)('diffuse')
        self.emissive = Group(Keyword('emissive').suppress() + ogre_parse.basereader.colorspec)('emissive')
        self.specular = Group(Keyword('specular').suppress() + ogre_parse.basereader.specular_spec)('specular')

    def test_color_3(self):
        amb3 = self.ambient.parseString(test_ambient_3)
        dif3 = self.diffuse.parseString(test_diffuse_3)
        emi3 = self.emissive.parseString(test_emissive_3)
        spe3 = self.specular.parseString(test_specular_3)

        c = ogre_parse.basemodel.Color(vals=[0.1, 0.2, 0.3, 1.0])

        # desired usage in comments
        self.assertEqual(c, amb3.ambient[0])
        self.assertEqual(c, dif3.diffuse[0])
        self.assertEqual(c, emi3.emissive[0])
        self.assertEqual(c, spe3.specular[0].color[0])
        self.assertEqual(25.0, spe3.specular[0].shininess[0])

    def test_color_4(self):
        amb4 = self.ambient.parseString(test_ambient_4)
        dif4 = self.diffuse.parseString(test_diffuse_4)
        emi4 = self.emissive.parseString(test_emissive_4)
        spe4 = self.specular.parseString(test_specular_4)

        c = ogre_parse.basemodel.Color(vals=[0.1, 0.2, 0.3, 1.0])

        # desired usage in comments
        self.assertEqual(c, amb4.ambient[0])
        self.assertEqual(c, dif4.diffuse[0])
        self.assertEqual(c, emi4.emissive[0])
        self.assertEqual(c, spe4.specular[0].color[0])
        self.assertEqual(25.0, spe4.specular[0].shininess[0])

# --------------------------------------------- #
test_texture_unit = """
texture_unit
{
    tex_address_mode clamp
    texture file.ext
    texture_alias alias
}
"""

test_texture_unit_name = """
texture_unit albedo
{
    texture file.ext
    filtering none
    tex_address_mode clamp
}
"""

test_texture_unit_filtering_none = """
texture_unit
{
    texture file.ext
    filtering none
}
"""

test_texture_unit_filtering_linear_linear_point = """
texture_unit
{
    texture file.ext
    filtering linear linear point
}
"""

test_texture_unit_address_mode_clamp = """
texture_unit
{
    texture file.ext
    tex_address_mode clamp
}
"""

test_texture_unit_texture_params = '''
texture_unit
{
    texture stoplight.jpg 2d 0
    tex_address_mode clamp
    filtering none
}
'''

test_texture_unit_texturealias = '''
texture_unit
{
    texture file.ext
    texture_alias alias
}
'''

test_texture_unit_scale = """
texture_unit
{
    texture file.ext
    scale 0.1 0.2
}
"""

test_texture_unit_colour_op = """
texture_unit
{
    texture file.ext
    colour_op alpha_blend
}
"""

test_texture_unit_colour_op_ex = '''
texture_unit
{
    texture file.ext
    colour_op_ex add_signed src_manual src_current 0.5
}
'''

test_texture_unit_fallback = '''
texture_unit
{
    texture file.ext
    colour_op_multipass_fallback one one_minus_dest_alpha
}
'''

test_texture_unit_binding_type = '''
texture_unit
{
    texture file.ext
    binding_type vertex
}
'''

test_texture_unit_texture_format = '''
texture_unit
{
    texture aureola.png PF_BYTE_LA
    tex_address_mode clamp
}
'''

test_texture_unit_env_map = '''
texture_unit
{
    texture file.ext
    env_map cubic_reflection
}
'''


class TestTexture(unittest.TestCase):
    def setUp(self):
        self.reader_ = ogre_parse.subreader.ReadTextureUnit()

    def test_texture_unit(self):
        res = self.reader_.parseString(test_texture_unit)
        tu = res.texture_unit

        self.assertEqual('', tu.name )
        self.assertEqual('file.ext', tu.resource_name )
        self.assertEqual('texture', tu.resource_type )

    def test_texture_unit_name(self):
        res = self.reader_.parseString(test_texture_unit_name)
        tu = res.texture_unit

        self.assertEqual('albedo', tu.name)

    def test_unit_filtering_none(self):
        res = self.reader_.parseString(test_texture_unit_filtering_none)
        tu = res.texture_unit

        self.assertEqual( 'none', tu.filtering )

    def test_unit_filtering_LLP(self):
        res = self.reader_.parseString(test_texture_unit_filtering_linear_linear_point)
        tu = res.texture_unit

        self.assertEqual( 'linear linear point', tu.filtering )

    def test_unit_address_mode(self):
        res = self.reader_.parseString(test_texture_unit_address_mode_clamp)
        tu = res.texture_unit

        self.assertEqual( 'clamp', tu.tex_address_mode )

    def test_texture_unit_texturealias(self):
        res = self.reader_.parseString(test_texture_unit_texturealias)
        tu = res.texture_unit

        self.assertEqual('alias', tu.texture_alias)

    def test_texture_unit_scale(self):
        res = self.reader_.parseString(test_texture_unit_scale)
        tu = res.texture_unit

        self.assertTrue(float_eq(0.1, tu.scale[0]))
        self.assertTrue(float_eq(0.2, tu.scale[1]))

    def test_texture_unit_colour_op(self):
        res = self.reader_.parseString(test_texture_unit_colour_op)
        tu = res.texture_unit

        self.assertEqual('alpha_blend', tu.colour_op)

    def test_texture_unit_colour_op_ex(self):
        res = self.reader_.parseString(test_texture_unit_colour_op_ex)
        tu = res.texture_unit

        self.assertEqual('add_signed src_manual src_current 0.5', tu.colour_op_ex)

    def test_texture_unit_fallback(self):
        res = self.reader_.parseString(test_texture_unit_fallback)
        tu = res.texture_unit

        self.assertEqual('one one_minus_dest_alpha', tu.colour_op_multipass_fallback)

    def test_texture_unit_binding_type(self):
        res = self.reader_.parseString(test_texture_unit_binding_type)
        tu = res.texture_unit

        self.assertEqual('vertex', tu.binding_type)

    def test_texture_unit_texture_format(self):
        res = self.reader_.parseString(test_texture_unit_texture_format)
        tu = res.texture_unit

        self.assertEqual('PF_BYTE_LA', tu.image_format)

    def test_texture_unit_env_map(self):
        res = self.reader_.parseString(test_texture_unit_env_map)
        tu = res.texture_unit

        self.assertEqual('cubic_reflection', tu.env_map)


# --------------------------------------------- #
test_shader_ref_vert = """
vertex_program_ref shaderVert
{
}
"""

test_shader_ref_frag = """
fragment_program_ref shaderFrag
{
}
"""

test_shader_ref_prop_param_named_auto = """
fragment_program_ref shaderFrag
{
    param_named_auto light_spot_vs light_direction_view_space_array 4
    param_named_auto spot_terms spotlight_params_array 4
}
"""

class TestShaderRef(unittest.TestCase):
    def setUp(self):
        self.reader_ = ogre_parse.subreader.ReadShaderReference()

    def test_shader_ref_vert(self):
        res = self.reader_.parseString(test_shader_ref_vert)
        shader = res.shader_ref

        self.assertEqual(shader.stage, 'vertex_program_ref')
        self.assertEqual(shader.resource_name, 'shaderVert')

    def test_shader_ref_frag(self):
        res = self.reader_.parseString(test_shader_ref_frag)
        shader = res.shader_ref

        self.assertEqual(shader.stage, 'fragment_program_ref')
        self.assertEqual(shader.resource_name, 'shaderFrag')

    def test_shader_ref_prop_param_named_auto(self):
        res = self.reader_.parseString(test_shader_ref_prop_param_named_auto)
        shader = res.shader_ref

        self.assertEqual(shader.param_named_auto['light_spot_vs'], 'light_direction_view_space_array 4')
        self.assertEqual(shader.param_named_auto['spot_terms'], 'spotlight_params_array 4')


# --------------------------------------------- #
test_pass = """
pass
{
    ambient 0.1 0.2 0.3 0.4
    diffuse 0.5 0.6 0.7 0.8
    emissive 0.25 0.5 0.75 1.0
    specular 0.33 0.66 0.99 1.0 33.33
}
"""

test_pass_name = """
pass aGoodName
{
    ambient 0.1 0.2 0.3 0.4
    diffuse 0.5 0.6 0.7 0.8
}
"""

test_pass_specular3 = """
pass
{
    specular 0.1 0.2 0.3 25.5
}
"""

test_pass_specular4 = """
pass
{
    specular 0.1 0.2 0.3 0.4 25.5
}
"""

test_pass_vertexcolour = '''
pass
{
    diffuse vertexcolour
}
'''

test_pass_tex = """
pass
{
    texture_unit
    {
        texture_alias alias
        texture file.ext
    }
}
"""

test_pass_2tex = """
pass
{
    texture_unit
    {
        texture file01.ext
    }

    texture_unit
    {
        texture file02.ext
    }
}
"""

test_pass_2shader = """
pass
{
    vertex_program_ref shaderVert
    {
    }

    fragment_program_ref shaderFrag
    {
    }
}
"""

test_pass_tex_2shader = """
pass
{
    texture_unit
    {
        texture file.ext
    }

    vertex_program_ref shaderVert
    {
    }

    fragment_program_ref shaderFrag
    {
    }
}
"""

test_pass_blend = """
pass
{
    scene_blend one one_minus_dest_alpha
    separate_scene_blend one one_minus_dest_alpha one one
    scene_blend_op subtract
    separate_scene_blend_op reverse_subtract min
}
"""

test_pass_depth = """
pass
{
    depth_check off
    depth_write off
    depth_func equal
    depth_bias 10.0 2.0
}
"""

test_pass_alpha = '''
pass
{
    alpha_rejection greater_equal 128
    alpha_to_coverage on
}
'''

test_pass_lightscissor = '''
pass
{
    light_scissor on
    light_clip_planes on
}
'''

test_pass_illum_stage = '''
pass
{
    illumination_stage per_light
}
'''

test_pass_normals = '''
pass
{
    normalise_normals on
}
'''

test_pass_transparent = '''
pass
{
    transparent_sorting force
}
'''

test_pass_cull = '''
pass
{
    cull_hardware none
    cull_software none
}
'''

test_pass_lighting = '''
pass
{
    lighting off
    shading phong
}
'''

test_pass_polygon = '''
pass
{
    polygon_mode wireframe
    polygon_mode_overrideable false
}
'''

test_pass_fog = '''
pass
{
    fog_override true exp 1 1 1 0.002 100 10000
}
'''

test_pass_colour = '''
pass
{
    ambient 1 0 0
    diffuse 0 1 0
    emissive 0 0 1
    specular 1 1 0 12.5
}
'''

test_pass_colour_write = '''
pass
{
    colour_write off
}
'''

test_pass_light_index = '''
pass
{
    start_light 5
    max_lights 20
}
'''

test_pass_iteration = '''
pass
{
    iteration 1 per_n_lights 2 point
}
'''

test_pass_point = '''
pass
{
    point_size 5.0
    point_sprites on
    point_size_attenuation on linear
    point_size_min 3.5
    point_size_max 22.5
}
'''



class TestPass(unittest.TestCase):
    def setUp(self):
        self.reader_ = ogre_parse.subreader.ReadPass()

    def test_pass(self):
        res = self.reader_.parseString(test_pass)

        ambi = Color([[0.10, 0.20, 0.30, 0.40]])
        diff = Color([[0.5, 0.6, 0.7, 0.8]])
        emis = Color([[0.25, 0.5, 0.75, 1.0]])
        spec = Color([[0.33, 0.66, 0.99, 1.0]])
        shin = float(33.33)

        self.assertEqual( ambi, res.mpass.ambient )
        self.assertEqual( diff, res.mpass.diffuse )
        self.assertEqual( emis, res.mpass.emissive )
        self.assertEqual( spec, res.mpass.specular )
        self.assertTrue( float_eq(shin, res.mpass.shininess))
        self.assertEqual( res.mpass.name, '' )

    def test_pass_name(self):
        res = self.reader_.parseString(test_pass_name)

        self.assertEqual( res.mpass.name, 'aGoodName')

    def test_pass_tex(self):
        res = self.reader_.parseString(test_pass_tex)

        len_tex = len(res.mpass.texture_units)
        self.assertEqual(len_tex, 1)

    def test_pass_2tex(self):
        res = self.reader_.parseString(test_pass_2tex)

        len_tex = len(res.mpass.texture_units)
        self.assertEqual(len_tex, 2)

    def test_pass_2shader(self):
        res = self.reader_.parseString(test_pass_2shader)

        len_shader = len(res.mpass.shaders)
        self.assertEqual(len_shader, 2)

    def test_pass_tex_2shader(self):
        res = self.reader_.parseString(test_pass_tex_2shader)

        len_tex = len(res.mpass.texture_units)
        self.assertEqual(len_tex, 1)

        len_shader = len(res.mpass.shaders)
        self.assertEqual(len_shader, 2)

    def test_pass_blend(self):
        res = self.reader_.parseString(test_pass_blend)

        self.assertEqual('one one_minus_dest_alpha', res.mpass.scene_blend)
        self.assertEqual('one one_minus_dest_alpha one one', res.mpass.separate_scene_blend)
        self.assertEqual('subtract', res.mpass.scene_blend_op)
        self.assertEqual('reverse_subtract min', res.mpass.separate_scene_blend_op)

    def test_pass_depth(self):
        res = self.reader_.parseString(test_pass_depth)

        self.assertEqual('off', res.mpass.depth_check)
        self.assertEqual('off', res.mpass.depth_write)
        self.assertEqual('equal', res.mpass.depth_func)
        self.assertTrue( float_eq(res.mpass.depth_bias_constant, 10.0))
        self.assertTrue( float_eq(res.mpass.depth_bias_slopescale, 2.0))

    def test_pass_alpha(self):
        res = self.reader_.parseString(test_pass_alpha)

        self.assertEqual('greater_equal', res.mpass.alpha_rejection_function)
        self.assertTrue( float_eq(128.0, res.mpass.alpha_rejection_threshold) )
        self.assertEqual('on', res.mpass.alpha_to_coverage )

    def test_pass_light_scissor(self):
        res = self.reader_.parseString(test_pass_lightscissor)

        self.assertEqual('on', res.mpass.light_scissor)
        self.assertEqual('on', res.mpass.light_clip_planes)

    def test_pass_illum_stage(self):
        res = self.reader_.parseString(test_pass_illum_stage)

        self.assertEqual('per_light', res.mpass.illumination_stage)

    def test_pass_normals(self):
        res = self.reader_.parseString(test_pass_normals)

        self.assertEqual('on', res.mpass.normalise_normals)

    def test_pass_transparent(self):
        res = self.reader_.parseString(test_pass_transparent)

        self.assertEqual('force', res.mpass.transparent_sorting)

    def test_pass_cull(self):
        res = self.reader_.parseString(test_pass_cull)

        self.assertEqual('none', res.mpass.cull_hardware)
        self.assertEqual('none', res.mpass.cull_software)

    def test_pass_lighting(self):
        res = self.reader_.parseString(test_pass_lighting)

        self.assertEqual('off', res.mpass.lighting)
        self.assertEqual('phong', res.mpass.shading)

    def test_pass_polygon(self):
        res = self.reader_.parseString(test_pass_polygon)

        self.assertEqual('wireframe', res.mpass.polygon_mode)
        self.assertEqual('false', res.mpass.polygon_mode_overrideable)

    def test_pass_fog(self):
        res = self.reader_.parseString(test_pass_fog)

        self.assertEqual('true exp 1 1 1 0.002 100 10000', res.mpass.fog_override)

    def test_pass_colour(self):
        res = self.reader_.parseString(test_pass_colour)

        self.assertEqual(Color(vals=[1, 0, 0]), res.mpass.ambient)
        self.assertEqual(Color(vals=[0, 1, 0]), res.mpass.diffuse)
        self.assertEqual(Color(vals=[0, 0, 1]), res.mpass.emissive)
        self.assertEqual(Color(vals=[1, 1, 0]), res.mpass.specular)

    def test_pass_vertexcolour(self):
        # res = self.reader_.parseString(test_pass_vertexcolour)
        #
        # self.assertEqual('vertexcolour', res.mpass.ambient)
        pass

    def test_pass_colour_write(self):
        res = self.reader_.parseString(test_pass_colour_write)

        self.assertEqual('off', res.mpass.colour_write)

    def test_pass_light_index(self):
        res = self.reader_.parseString(test_pass_light_index)

        self.assertEqual(5, res.mpass.start_light)
        self.assertEqual(20, res.mpass.max_lights)

    def test_pass_iteration(self):
        res = self.reader_.parseString(test_pass_iteration)

        self.assertEqual('1 per_n_lights 2 point', res.mpass.iteration)

    def test_pass_point(self):
        res = self.reader_.parseString(test_pass_point)

        self.assertTrue( float_eq(5.0, res.mpass.point_size) )
        self.assertEqual('on', res.mpass.point_sprites)
        self.assertEqual('on linear', res.mpass.point_size_attenuation)
        self.assertTrue( float_eq(3.5, res.mpass.point_size_min) )
        self.assertTrue( float_eq(22.5, res.mpass.point_size_max) )


# --------------------------------------------- #
test_technique_empty = """
technique
{
}
"""

test_technique = """
technique
{
    pass
    {
    }
}
"""

test_technique_2pass = """
technique
{
    pass
    {
    }

    pass
    {
    }
}
"""

test_technique_scheme = """
technique
{
    scheme catsAndDogs

    pass
    {
    }
}
"""

test_technique_lod = """
technique
{
    lod_index 4

    pass
    {
    }
}
"""

test_technique_shadow = '''
technique
{
    shadow_caster_material castThatShadow
    shadow_receiver_material receiveThisShadow

    pass
    {
    }
}
'''

class TestTechnique(unittest.TestCase):
    def setUp(self):
        self.reader_ = ogre_parse.subreader.ReadTechnique()

    def test_technique_empty(self):
        self.assertRaises(pyparsing.ParseBaseException, self.reader_.parseString, test_technique_empty)

    def test_technique(self):
        res = self.reader_.parseString(test_technique)

        len_passes = len(res.technique.passes)
        self.assertEqual(1, len_passes)

    def test_technique_2pass(self):
        res = self.reader_.parseString(test_technique_2pass)

        len_passes = len(res.technique.passes)
        self.assertEqual(2, len_passes)

    def test_technique_scheme(self):
        res = self.reader_.parseString(test_technique_scheme)

        self.assertEqual('catsAndDogs', res.technique.scheme)

    def test_technique_lod(self):
        res = self.reader_.parseString(test_technique_lod)

        self.assertEqual(4, res.technique.lod_index)

    def test_technique_shadow(self):
        res = self.reader_.parseString(test_technique_shadow)

        self.assertEqual('castThatShadow', res.technique.shadow_caster_material)
        self.assertEqual('receiveThisShadow', res.technique.shadow_receiver_material)


# --------------------------------------------- #
test_mat = """
material awesomeMaterial
{
    technique
    {
        pass
        {
            texture_unit
            {
                texture file.ext
                filtering none
                texture_alias alias
            }
        }
    }
}
"""

test_mat_no_tech = """
material someName
{
}
"""

test_mat_2tech = """
material mat2tech
{
    technique
    {
        pass
        {
        }
    }

    technique
    {
        pass
        {
        }
    }
}
"""

test_mat_lod = """
material matLods
{
    lod_strategy DistanceCustom
    lod_values 0 1 2

    technique
    {
        pass
        {
        }
    }
}
"""

test_mat_shadows = '''
material matShadows
{
    receive_shadows off
    transparency_casts_shadows on

    technique
    {
        pass
        {
        }
    }
}
'''

test_mat_texture_alias = '''
material matTextureAlias
{
    set_texture_alias a z
    set_texture_alias b y
    set_texture_alias c x

    technique
    {
        pass
        {
        }
    }
}
'''

class TestMaterial(unittest.TestCase):
    def setUp(self):
        self.reader_ = ogre_parse.reader.ReadMaterial()

    def test_mat(self):
        res = self.reader_.parseString(test_mat)

        self.assertEqual('awesomeMaterial', res.material.name)
        self.assertEqual(1, len(res.material.techniques))

    def test_mat_empty(self):
        self.assertRaises(pyparsing.ParseBaseException, self.reader_.parseString, test_mat_no_tech)

    def test_mat_2tech(self):
        res = self.reader_.parseString(test_mat_2tech)

        self.assertEqual(2, len(res.material.techniques))

    def test_mat_lod(self):
        res = self.reader_.parseString(test_mat_lod)

        self.assertEqual('DistanceCustom', res.material.lod_strategy)
        self.assertEqual([0, 1, 2], res.material.lod_values)

    def test_mat_shadows(self):
        res = self.reader_.parseString(test_mat_shadows)

        self.assertEqual('off', res.material.receive_shadows)
        self.assertEqual('on', res.material.transparency_casts_shadows)

    def test_mat_texture_alias(self):
        res = self.reader_.parseString(test_mat_texture_alias)

        self.assertEqual('z', res.material.texture_alias['a'])
        self.assertEqual('y', res.material.texture_alias['b'])
        self.assertEqual('x', res.material.texture_alias['c'])


# --------------------------------------------- #

test_shader_vert_hlsl = '''
vertex_program billboard_vColor_1UV_vp_hlsl hlsl
{
    source cloud.hlsl
    entry_point CloudVS
    target vs_2_0

    default_params
    {
        // auto params
        param_named_auto Mv view_matrix
        param_named_auto Mp projection_matrix

        // custom parameter
        param_named billboard_radius float 1.0
    }
}
'''

test_shader_frag_hlsl = '''
fragment_program vertex_color_fp_hlsl hlsl
{
    source cloud.hlsl
    entry_point CloudPS
    target ps_2_0

    default_params
    {
    }
}
'''

test_shader_vert_glsl = '''
vertex_program billboard_vColor_1UV_vp glsl
{
    source billboard.vert

    default_params
    {
        // auto params
        param_named_auto Mv view_matrix
        param_named_auto Mp projection_matrix

        // custom parameter
        param_named billboard_radius float 1.0
    }
}
'''

test_shader_frag_glsl = '''
fragment_program vertex_color_fp glsl
{
    source vertex_color.frag

    default_params
    {
    }
}
'''

class TestShaderDeclaration(unittest.TestCase):
    def setUp(self):
        self.reader_ = ogre_parse.reader.ReadShaderDeclaration()

    def test_shader_vert_hlsl(self):
        res = self.reader_.parseString(test_shader_vert_hlsl)

        self.assertEqual('vertex_program', res.shader.stage)
        self.assertEqual('hlsl', res.shader.language)
        self.assertEqual('billboard_vColor_1UV_vp_hlsl', res.shader.name)
        self.assertEqual('cloud.hlsl', res.shader.source)
        self.assertEqual('CloudVS', res.shader.entry_point)
        self.assertEqual('vs_2_0', res.shader.target)
        self.assertEqual('view_matrix', res.shader.param_named_auto['Mv'])
        self.assertEqual('projection_matrix', res.shader.param_named_auto['Mp'])
        self.assertEqual('float 1.0', res.shader.param_named['billboard_radius'])

    def test_shader_frag_hlsl(self):
        res = self.reader_.parseString(test_shader_frag_hlsl)

        self.assertEqual('fragment_program', res.shader.stage)
        self.assertEqual('hlsl', res.shader.language)
        self.assertEqual('vertex_color_fp_hlsl', res.shader.name)
        self.assertEqual('cloud.hlsl', res.shader.source)
        self.assertEqual('CloudPS', res.shader.entry_point)
        self.assertEqual('ps_2_0', res.shader.target)

    def test_shader_vert_glsl(self):
        res = self.reader_.parseString(test_shader_vert_glsl)

        self.assertEqual('vertex_program', res.shader.stage)
        self.assertEqual('glsl', res.shader.language)
        self.assertEqual('billboard_vColor_1UV_vp', res.shader.name)
        self.assertEqual('billboard.vert', res.shader.source)

    def test_shader_frag_glsl(self):
        res = self.reader_.parseString(test_shader_frag_glsl)

        self.assertEqual('fragment_program', res.shader.stage)
        self.assertEqual('glsl', res.shader.language)
        self.assertEqual('vertex_color_fp', res.shader.name)
        self.assertEqual('vertex_color.frag', res.shader.source)

# --------------------------------------------- #

test_script_mat = """
material test_script_mat
{
    technique
    {
        scheme gizmo_name

        pass
        {
        }
    }
}
"""

test_script_2mat = """
material matName1
{
    technique
    {
        pass
        {
        }
    }
}

material matName2
{
    technique
    {
        pass
        {
        }
    }
}
"""

test_script_mat_comments = """
// this is a great place for comments
material test_script_mat // a comment here would  be cool
{
    // this is a technique
    technique // you never know
    {
        // this is a pass
        pass // will this cause a problem
        {
            // nothing to see here
        } // let's
    } // be
} // clear
// no problems with comments!
"""

test_script_mat_and_shader = """

fragment_program vertex_color_fp glsl
{
    source vertex_color.frag

    default_params
    {
    }
}

material cloud_material
{
    technique gl
    {
        pass
        {
        }
    }
}

fragment_program vertex_color_fp2 glsl
{
    source vertex_color.frag

    default_params
    {
    }
}


material cloud_material2
{
    technique gl
    {
        pass
        {
        }
    }
}

"""


class TestScript(unittest.TestCase):
    def setUp(self):
        # instantiate reader
        self.reader_ = ogre_parse.reader.ReadScript()

    def test_script_mat(self):
        res = self.reader_.parseString(test_script_mat)

        self.assertEqual(1, len(res.script.materials))

    def test_script_2mat(self):
        res = self.reader_.parseString(test_script_2mat)

        self.assertEqual(2, len(res.script.materials))

    def test_script_mat_comments(self):
        res = self.reader_.parseString(test_script_mat_comments)

        self.assertEqual(1, len(res.script.materials))

    def test_script_mat_and_shader(self):
        res = self.reader_.parseString(test_script_mat_and_shader)

        self.assertEqual(2, len(res.script.materials))
        self.assertEqual(2, len(res.script.shaders))

