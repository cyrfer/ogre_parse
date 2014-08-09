__author__ = 'jgrant'


from ogre_parse.basemodel import *


# should be hooked up to a 'subreader.ReadTextureUnit' instance
class MTextureUnit(object):
    def __init__(self, tokens=None):
        self.name = ''
        self.resource_type = 'texture'
        self.resource_name = ''
        self.filtering = 'none'
        self.tex_address_mode = 'wrap'

        if tokens:
            print( tokens.dump('---- '))

            if tokens.texture_unit.required:
                self.resource_type = tokens.texture_unit.required.resource_type
                self.resource_name = tokens.texture_unit.required.resource_properties.name

    def __str__(self):
        indent = '\t'

        repr = 'texture_unit' + self.name + '\n{\n'
        repr += indent + self.resource_type + ' ' + self.resource_name
        repr += indent + 'filtering ' + self.filtering
        repr += indent + 'tex_address_mode ' + self.tex_address_mode

        repr += '\n}\n'

        return repr

    # __repr__ = __str__



# should be hooked up to a 'subreader.ReadPass' instance
class MPass(object):
    def __init__(self, tokens=None):
        self.name = ''
        self.ambient = Color()
        self.emissive = Color()
        self.diffuse = Color()
        self.specular = Color()
        self.shininess = float(10.0)

        # grab parsed results
        if tokens:
            if tokens.mpass.name:
                self.name = tokens.mpass.name

            if tokens.mpass.body.ambient:
                self.ambient = tokens.mpass.body.ambient.args

            if tokens.mpass.body.diffuse:
                self.diffuse = tokens.mpass.body.diffuse.args

            if tokens.mpass.body.emissive:
                self.emissive = tokens.mpass.body.emissive.args

            if tokens.mpass.body.specular:
                self.specular = tokens.mpass.body.specular.specular

            if tokens.mpass.body.specular:
                self.shininess = tokens.mpass.body.specular.shininess


    def __str__(self):
        repr = 'pass ' + self.name + '\n{\n'

        indent = '\t'

        repr += indent + 'ambient ' + str(self.ambient) + '\n'
        repr += indent + 'diffuse ' + str(self.diffuse) + '\n'
        repr += indent + 'emissive ' + str(self.emissive) + '\n'
        repr += indent + 'specular ' + str(self.specular) + ' ' + str(self.shininess) + '\n'

        repr += '}\n'

        return repr

    __repr__ = __str__



sample_pass = '''
pass
{
    ambient 0.1 0.2 0.3 0.4
    diffuse 0.5 0.6 0.7 0.8
    specular 0.3 0.4 0.5 0.6 21.0
    emissive 0.9 0.0 0.1 0.2
}
'''

sample = '''
    ambient 0.1 0.2 0.3 0.4
    diffuse 0.5 0.6 0.7 0.8
    specular 0.3 0.4 0.5 0.6 22.0
    emissive 0.9 0.0 0.1 0.2
'''

if __name__ == '__main__':

    # define color keywords
    # AMBIENT, DIFFUSE, SPECULAR, EMISSIVE = map(Keyword, 'ambient diffuse specular emissive'.split())

# '''
#     scene_blend separate_scene_blend
#     depth_check depth_write depth_func depth_bias iteration_depth_bias
#     alpha_rejection alpha_to_coverage
#     light_scissor light_clip_planes
#     illumination_stage transparent_sorting
#     nomralize_normals
#     cull_hardware cull_software
#     lighting shading
#     polygon_mode polygon_mode_overrideable
#     fog_override
#     colour_write
#     max_lights start_light iteration
#     point_size point_sprites point_size_attenuation point_size_min point_size_max
# '''

    # parser.setDebug(True)

    # test it
    # parsed = parser.parseString(sample)
    parsed = parser.parseString(sample_pass)
    print( 'type(parsed.mpass) = %s' % type(parsed.mpass) )# parsed.dump(indent='-///- ')
    print( 'val of mpass = \n%s' % parsed.mpass )

