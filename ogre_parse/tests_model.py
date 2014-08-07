__author__ = 'jgrant'

import unittest
from ogre_parse.tests_reader import *
import ogre_parse.model

test_model_texture = """
texture_unit albedo
{
    texture file.ext
    filtering none
    tex_address_mode clamp
}
"""

class TestModel(unittest.TestCase):

    def test_texture(self):
        # obtain some parsing results
        grammar = ogre_parse.subreader.ReadTextureUnit()
        parsed = grammar.parseString(test_texture_unit)

        # test creating the model from parsed results
        model = ogre_parse.model.TextureUnit(parsed)

        # desired usage of model
        self.assertEqual(model.get('texture'), 'file.ext')


    def test_shader_ref(self):
        pass


    def test_mat_pass(self):
        pass


    def test_mat_technique(self):
        pass


    def test_mat(self):
        pass


    def test_comp(self):
        pass


    def test_shader_definition(self):
        pass

