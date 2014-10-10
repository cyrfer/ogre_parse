__author__ = 'jgrant'

import unittest
import ogre_parse.model
import ogre_parse.subreader
import ogre_parse.reader

test_model_texture = """
texture_unit albedo
{
    texture_alias alias
    texture file.ext
    tex_address_mode clamp
    filtering none
}
"""

test_model_shaderref_vert = '''
vertex_program_ref myVertShader
{
}
'''

test_model_shaderref_param_named = '''
fragment_program_ref myFragShader
{
    param_named_auto MVP worldviewproj_matrix
    param_named myVec float4 .1 0.2 .3 0.4
    param_named myVar float 0.5
}
'''

test_model_pass = '''
pass myOptionalPassName
{
}
'''

test_model_technique = '''
technique myOptionalTechName
{
    pass
    {
    }
}
'''

test_model_material = '''
material mn
{
    technique
    {
        pass
        {
            shading phong
            polygon_mode wireframe
            polygon_mode_overrideable true
            fog_override true exp 1 1 1 0.002 100 10000
        }
    }
}
'''

test_model_script = '''
%s
%s
''' % (test_model_material.replace('mn', 'mn1'), test_model_material.replace('mn', 'mn2'))

class TestModel(unittest.TestCase):

    def test_texture(self):
        # obtain some parsing results
        grammar = ogre_parse.subreader.ReadTextureUnit()
        # print('--- string data:\n%s' % test_model_texture.strip())
        parsed = grammar.parseString(test_model_texture)
        model = parsed[0]
        modstr = str(model)
        # print('--- str(model):\n%s---' % modstr)
        self.assertEqual(test_model_texture.strip(), modstr.strip())


    def test_shader_ref(self):
        grammar = ogre_parse.subreader.ReadShaderReference()
        # print('--- string data:\n%s' % test_model_shaderref_vert.strip())
        parsed = grammar.parseString(test_model_shaderref_vert)
        model = parsed[0]
        modstr = str(model)
        # print('--- str(model)---\n%s' % modstr)
        self.assertEqual(test_model_shaderref_vert.strip(), modstr.strip())

    def test_shaderref_param(self):
        grammar = ogre_parse.subreader.ReadShaderReference()
        parsed = grammar.parseString(test_model_shaderref_param_named)
        model = parsed[0]
        modstr = str(model)
        print('--- str(model)---\n%s' % modstr)
        self.assertEqual(test_model_shaderref_param_named.strip(), modstr.strip())

    def test_mat_pass(self):
        grammar = ogre_parse.subreader.ReadPass()
        # print('--- string data:\n%s---' % test_model_pass)
        parsed = grammar.parseString(test_model_pass)
        model = parsed[0]
        modstr = str(model)
        # print('--- str(model):\n%s---' % modstr)
        self.assertEqual(test_model_pass.strip(), modstr.strip())


    def test_mat_technique(self):
        grammar = ogre_parse.subreader.ReadTechnique()
        # print('--- string data:\n%s---' % test_model_technique)
        parsed = grammar.parseString(test_model_technique)
        model = parsed[0]
        modstr = str(model)
        # print('--- str(model):\n%s---' % modstr)
        self.assertEqual(test_model_technique.strip(), modstr.strip())


    def test_mat(self):
        grammar = ogre_parse.reader.ReadMaterial()
        # print('--- string data:\n%s---' % test_model_material)
        parsed = grammar.parseString(test_model_material)
        model = parsed[0]
        modstr = str(model)
        # print('--- str(model):\n%s---' % modstr)
        self.assertEqual(test_model_material.strip(), modstr.strip())


    def test_comp(self):
        pass


    def test_shader_definition(self):
        pass


    def test_script(self):
        grammar = ogre_parse.reader.ReadScript()
        # print('--- string data:\n%s---' % test_model_script)
        parsed = grammar.parseString(test_model_script)
        # print('--- type(parsed[0])=%s' % type(parsed[0]))
        model = parsed[0]
        modstr = str(model)
        # print('--- str(model):\n%s---' % modstr)
        self.assertEqual(test_model_script.strip(), modstr.strip())

