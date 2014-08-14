__author__ = 'jgrant'

import unittest

# same imports as client code
import ogre_parse.reader
import ogre_parse.subreader

import pyparsing

def float_eq(a, b, epsilon=0.00000001):
    return abs(a - b) < epsilon

# --------------------------------------------- #
test_texture_unit = """
texture_unit
{
    texture file.ext
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

class TestTexture(unittest.TestCase):
    def setUp(self):
        self.reader_ = ogre_parse.subreader.ReadTextureUnit()

    def test_texture_unit(self):
        res = self.reader_.parseString(test_texture_unit)
        tu = res.texture_unit

        self.assertEqual( tu.name, '' )
        self.assertEqual( tu.resource_name, 'file.ext' )

    def test_texture_unit_name(self):
        res = self.reader_.parseString(test_texture_unit_name)
        tu = res.texture_unit

        self.assertEqual( tu.name, 'albedo')

    def test_unit_filtering_none(self):
        res = self.reader_.parseString(test_texture_unit_filtering_none)
        tu = res.texture_unit

        print('test: tu.properties = %s' % tu.properties )
        self.assertEqual( tu.properties['filtering'], 'none' )

    def test_unit_filtering_LLP(self):
        res = self.reader_.parseString(test_texture_unit_filtering_linear_linear_point)
        tu = res.texture_unit

        self.assertEqual( tu.properties['filtering'], 'linear linear point' )

    def test_unit_address_mode(self):
        res = self.reader_.parseString(test_texture_unit_address_mode_clamp)
        tu = res.texture_unit

        self.assertEqual( tu.properties['tex_address_mode'], 'clamp' )


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

test_pass_tex = """
pass
{
    texture_unit
    {
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

        self.assertTrue( float_eq(res.mpass.ambient[0], float(0.1)) )
        self.assertTrue( float_eq(res.mpass.diffuse[0], float(0.5)) )
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
material
{
    technique
    {
        pass
        {
        }
    }
}
"""

test_mat_no_tech = """
material
{
}
"""

test_mat_2tech = """
material
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

test_mat_prop_tech_prop = """
material
{
    lod_strategy Distance

    technique
    {
        pass
        {
        }
    }

    receive_shadows on
}
"""

class TestMaterial(unittest.TestCase):
    def setUp(self):
        self.reader_ = ogre_parse.reader.ReadMaterial()

    def test_mat(self):
        res = self.reader_.parseString(test_mat)

        len_mat = len(res)
        self.assertEqual(len_mat, 1)

    def test_mat_empty(self):
        self.assertRaises(pyparsing.ParseBaseException, self.reader_.parseString, test_mat_no_tech)
        # res = self.reader_.parseString(test_mat_no_tech)

    def test_mat_2tech(self):
        res = self.reader_.parseString(test_mat_2tech)

        len_elements = len(res)
        self.assertEqual(len_elements, 2)

    def test_mat_prop_tech_prop(self):
        res = self.reader_.parseString(test_mat_prop_tech_prop)

        len_elements = len(res)
        self.assertEqual(len_elements, 3)


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
material
{
    technique
    {
        pass
        {
        }
    }
}

material
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

test_script_real = """


material NoMaterial
{
	technique
	{
        scheme forward_FF
		pass
		{
            emissive 1 0 0 0
		}

	}

	//technique d3d9_gbuffer
	//{
//       scheme deferred_gbuffer
	//	pass
	//	{
//           emissive 1 0 0 0

//           vertex_program_ref phong_hlsl
//           {
//           }

//           fragment_program_ref gbuffer_hlsl
//           {
//           }
	//	}

	//}

//   technique stencil
//   {
//       scheme stencil

//       pass
//       {
//           emissive 1 0 0 1
//       }
//   }

}



material Cube_OgreMax
{
	//technique forward_FF
	//{
//       scheme forward_FF

	//	pass Map#682
	//	{
	//		diffuse 0.588 0.588 0.588 1
	//		specular 0 0 0 1 10
	//		//emissive 1 1 1 1

	//		texture_unit Map#683
	//		{
	//			texture cube_emissive_HDR.dds
	//			filtering linear linear linear
	//		}

//           //vertex_program_ref phong_1UV_fog_ver120
//           //{
//           //}

//           //fragment_program_ref BP_fog_emissive_alphaRejectEmissive
//           //{
//           //}
	//	}
	//}

	//technique gbuffer
	//{
//       scheme deferred_gbuffer

	//	pass Map#682
	//	{
	//		diffuse 0.588 0.588 0.588 1
	//		specular 0 0 0 1 10
	//		//emissive 1 1 1 1

	//		texture_unit Map#683
	//		{
	//			texture cube_emissive_HDR.dds
	//			filtering linear linear linear
	//		}

//           vertex_program_ref phong_1UV_hlsl
//           {
//           }

//           fragment_program_ref gbuffer_1UV_emissive_hlsl
//           {
//           }
//       }
	//}

    technique stencil
    {
        scheme stencil

        pass
        {
            emissive 0 0.5 0 1

            //vertex_program_ref phong_1UV_fog
            //{
            //}

            //fragment_program_ref stencil_BP_fog_decal
            //{
            //}
        }
    }
}



material Cage_OgreMax
{
	technique
	{
        scheme forward_FF

		pass
		{
			diffuse 0.588 0.588 0.588 1
			specular 0 0 0 1 10
		}

	}

	//technique d3d9_gbuffer
	//{
//       scheme deferred_gbuffer

	//	pass
	//	{
	//		diffuse 0.588 0.588 0.588 1
	//		specular 0 0 0 1 10

//           vertex_program_ref phong_hlsl
//           {
//           }

//           fragment_program_ref gbuffer_hlsl
//           {
//           }
	//	}

	//}


//   technique stencil
//   {
//       scheme stencil

//       pass
//       {
//           emissive 0 0 0.5 1

//           vertex_program_ref phong_1UV_fog_ver120
//           {
//           }

//           fragment_program_ref stencil_BP_fog_decal
//           {
//           }
//       }
//   }
}



material terrain_OgreMax
{
	technique
	{
        scheme forward_FF

		pass Map#686
		{
			ambient 0.588 0.588 0.588 1
			diffuse 0.588 0.588 0.588 1
			specular 0 0 0 1 10

			texture_unit Map#687
			{
				texture central_lr_11_9.dds
				filtering linear linear linear
			}
		}

	}

	//technique d3d9_gbuffer
	//{
//       scheme deferred_gbuffer

	//	pass
	//	{
	//		ambient 0.588 0.588 0.588 1
	//		diffuse 0.588 0.588 0.588 1
	//		specular 0 0 0 1 10

	//		texture_unit
	//		{
	//			texture central_lr_11_9.dds
	//			filtering linear linear linear
	//		}

//           vertex_program_ref phong_1UV_hlsl
//           {
//           }

//           fragment_program_ref gbuffer_1UV_decal_hlsl
//           {
//           }
	//	}

	//}

}



material terrain2_OgreMax
{
	technique forward_FF
	{
        scheme forward_FF

		pass
		{
			specular 0.231373 0.231373 0.231373 1 10

			texture_unit Map#687
			{
				texture central_lr_11_9.dds
				filtering linear linear linear
			}
		}

	}

	//technique d3d9_gbuffer
	//{
//       scheme deferred_gbuffer

	//	pass Map#686
	//	{
	//		specular 0.231373 0.231373 0.231373 1 10

	//		texture_unit
	//		{
	//			texture central_lr_11_9.dds
	//			filtering linear linear linear
	//		}

//           vertex_program_ref phong_1UV_hlsl
//           {
//           }

//           fragment_program_ref gbuffer_1UV_decal_hlsl
//           {
//           }
	//	}

	//}

}


"""




class TestScript(unittest.TestCase):
    def setUp(self):
        # instantiate reader
        self.reader_ = ogre_parse.reader.ReadScript()

    def test_script_mat(self):
        res = self.reader_.parseString(test_script_mat)

        len_elements = len(res)
        self.assertEqual(len_elements, 1)

    def test_script_2mat(self):
        res = self.reader_.parseString(test_script_2mat)

        len_elements = len(res)
        self.assertEqual(len_elements, 2)

    def test_script_mat_comments(self):
        res = self.reader_.parseString(test_script_mat_comments)

        len_elements = len(res)
        self.assertEqual(len_elements, 1)

    def test_script_real(self):
        # res = self.reader_.parseString(test_script_real)
        #
        # len_elements = len(res)
        # self.assertEqual(len_elements, 5)
        pass

