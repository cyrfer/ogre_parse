__author__ = 'cyrfer'

import unittest

# same imports as client code
import ogre_parse.reader
import ogre_parse.subreader

import pyparsing


# --------------------------------------------- #
test_texture_unit = """
texture_unit
{
    texture file.ext
}
"""

class TestTexture(unittest.TestCase):
    def setUp(self):
        self.reader_ = ogre_parse.subreader.ReadTextureUnit()

    def test_unit(self):
        res = self.reader_.parseString(test_texture_unit)
        len_units = len(res)

        self.assertEqual(len_units, 1)


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

class TestShaderRef(unittest.TestCase):
    def setUp(self):
        self.reader_ = ogre_parse.subreader.ReadShaderReference()

    def test_shader_vert(self):
        res = self.reader_.parseString(test_shader_ref_vert)

        len_shaders = len(res)
        self.assertEqual(len_shaders, 1)

    def test_shader_frag(self):
        res = self.reader_.parseString(test_shader_ref_frag)

        len_shaders = len(res)
        self.assertEqual(len_shaders, 1)


# --------------------------------------------- #
test_pass = """
pass
{
    ambient 0 0 0 1
    diffuse 1 1 1 0
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

        len_pass = len(res)
        self.assertEqual(len_pass, 1)

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


# --------------------------------------------- #

test_script_mat = """
material test_script_mat
{
    technique
    {
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


# --------------------------------------------- #
if __name__ == '__main__':
    unittest.main()
