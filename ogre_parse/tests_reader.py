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

        len_pass = len(res)
        self.assertEqual(len_pass, 1)

        len_tex = len(res[0])
        self.assertEqual(len_tex, 1)

    def test_pass_2shader(self):
        res = self.reader_.parseString(test_pass_2shader)

        len_pass = len(res)
        self.assertEqual(len_pass, 1)

        # TODO: need a better way to obtain the shaders
        len_shader = len(res[0])
        self.assertEqual(len_shader, 2)

    def test_pass_tex_2shader(self):
        res = self.reader_.parseString(test_pass_tex_2shader)

        len_pass  = len(res)
        self.assertEqual(len_pass, 1)

        # # TODO: not a good way to find textures
        # len_tex = len(res[0])
        # self.assertEqual(len_tex, 1)
        #
        # # TODO: not a good way to find shaders
        # len_shader = len(res[1])
        # self.assertEqual(len_shader, 2)


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

test_technique_lod = """
technique
{
    lod_index 4

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

class TestTechnique(unittest.TestCase):
    def setUp(self):
        self.reader_ = ogre_parse.subreader.ReadTechnique()

    def test_technique_empty(self):
        self.assertRaises(pyparsing.ParseBaseException, self.reader_.parseString, test_technique_empty)

    def test_technique(self):
        res = self.reader_.parseString(test_technique)
        len_tech = len(res)
        self.assertEqual(len_tech, 1)

        len_passes = len(res[0])
        self.assertEqual(len_passes, 1)

    def test_technique_2pass(self):
        res = self.reader_.parseString(test_technique_2pass)

        len_tech = len(res)
        self.assertEqual(len_tech, 1)

        len_passes = len(res[0])
        self.assertEqual(len_passes, 2)

    def test_technique_prop(self):
        res = self.reader_.parseString(test_technique_lod)

        # TODO: need a better way to retrieve properties and passes
        len_props  = len(res[0])
        self.assertEqual(len_props, 2) # should only be '1' for properties, and '1' for passes

    def test_technique_scheme(self):
        res = self.reader_.parseString(test_technique_scheme)

        len_elements = len(res[0])
        self.assertEqual(len_elements, 2)


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
        res = self.reader_.parseString(test_script_real)

        len_elements = len(res)
        self.assertEqual(len_elements, 5)

