__author__ = 'jgrant'


from ogre_parse.basemodel import *

from pyparsing import ParseException


# should be hooked up to a 'subreader.ReadTextureUnit' instance
class MTextureUnit(object):
    def __init__(self, tokens=None):
        self.name = ''
        self.resource_type = 'texture'
        self.resource_name = ''
        self.properties = {}

        if tokens:
            tu = tokens.texture_unit

            if tu.name:
                self.name = tu.name

            if tu.required:
                self.resource_type = tu.required.resource_type
                self.resource_name = tu.required.resource_properties.name

            if tu.properties:
                for k,v in tu.properties.items():
                    self.properties.update( {k : ' '.join(v)})


    def __str__(self):
        indent = '\t'
        repr = 'texture_unit' + self.name + '\n{\n'
        repr += indent + self.resource_type + ' ' + self.resource_name

        for k,v in self.properties.items():
            repr += str(k) + ' ' + str(v)

        repr += '\n}\n'

        return repr

    # http://stackoverflow.com/questions/1436703/difference-between-str-and-repr-in-python
    __repr__ = __str__



# should be hooked up to a 'subreader.ReadShaderReference' instance
class MShaderRef(object):
    def __init__(self, tokens=None):
        self.stage = ''
        self.resource_name = ''
        self.param_indexed = {}
        self.param_indexed_auto = {}
        self.param_named = {}
        self.param_named_auto = {}
        self.param_shared_ref = {}

        if tokens:
            shader = tokens.shader_ref

            if shader.stage:
                self.stage = shader.stage
            else:
                # how to throw exception?
                # http://pyparsing.wikispaces.com/share/view/5613328
                raise ParseException('ogre_parse::MShaderRef, missing shader stage, e.g. vertex_program_ref')

            if shader.resource_name:
                self.resource_name = shader.resource_name
            else:
                # how to throw exception?
                # http://pyparsing.wikispaces.com/share/view/5613328
                raise ParseException('ogre_parse::MShaderRef, missing shader resource name, e.g. myPhongShader')

            if shader.param_named_auto:
                for k in shader.param_named_auto.keys():
                    val = ' '.join(shader.param_named_auto[k])
                    self.param_named_auto.update({k: val})


    def __str__(self):
        repr = ''

        repr += self.stage + ' ' + self.resource_name
        repr += '\n{\n'

        for k,v in self.properties.items():
            repr += '\n' + str(k) + ' ' + str(v)

        repr += '\n}\n'
        return repr

    # http://stackoverflow.com/questions/1436703/difference-between-str-and-repr-in-python
    __repr__ = __str__


# should be hooked up to a 'subreader.ReadPass' instance
class MPass(object):
    def __init__(self, tokens=None):
        self.name = ''

        # color
        self.ambient = Color()
        self.emissive = Color()
        self.diffuse = Color()
        self.specular = Color()
        self.shininess = float(10.0)

        # blend
        self.scene_blend = 'one zero'
        self.separate_scene_blend = ''
        self.scene_blend_op = 'add'
        self.separate_scene_blend_op = 'add add'

        # depth
        self.depth_check = 'on'
        self.depth_write = 'on'
        self.depth_func = 'less_equal'
        self.iteration_depth_bias = 0.0
        self.depth_bias_constant = 0.0
        self.depth_bias_slopescale = 0.0

        # alpha
        self.alpha_rejection_function = 'always_pass'
        self.alpha_rejection_threshold = float(0.0)
        self.alpha_to_coverage = 'off'

        # objects
        self.texture_units = []
        self.shaders = []

        # grab parsed results
        if tokens:
            # print( tokens.dump('++ '))

            if tokens.mpass.name:
                self.name = tokens.mpass.name

            # --- color
            if tokens.mpass.ambient:
                self.ambient = tokens.mpass.ambient.args

            if tokens.mpass.diffuse:
                self.diffuse = tokens.mpass.diffuse.args

            if tokens.mpass.emissive:
                self.emissive = tokens.mpass.emissive.args

            if tokens.mpass.specular:
                self.specular = tokens.mpass.specular.specular

            if tokens.mpass.specular:
                self.shininess = tokens.mpass.specular.shininess

            # --- blend
            if tokens.mpass.scene_blend:
                self.scene_blend = ' '.join(tokens.mpass.scene_blend)

            if tokens.mpass.scene_blend_op:
                self.scene_blend_op = ' '.join(tokens.mpass.scene_blend_op)

            if tokens.mpass.separate_scene_blend:
                self.separate_scene_blend = ' '.join(tokens.mpass.separate_scene_blend)

            if tokens.mpass.separate_scene_blend_op:
                self.separate_scene_blend_op = ' '.join(tokens.mpass.separate_scene_blend_op)

            # --- depth
            if tokens.mpass.depth_check:
                self.depth_check = ' '.join(tokens.mpass.depth_check)

            if tokens.mpass.depth_write:
                self.depth_write = ' '.join(tokens.mpass.depth_write)

            if tokens.mpass.depth_func:
                self.depth_func = ' '.join(tokens.mpass.depth_func)

            if tokens.mpass.depth_bias:
                if tokens.mpass.depth_bias.constant:
                    self.depth_bias_constant = tokens.mpass.depth_bias.constant

                if tokens.mpass.depth_bias.slopescale:
                    self.depth_bias_slopescale = tokens.mpass.depth_bias.slopescale

            if tokens.mpass.iteration_depth_bias:
                self.iteration_depth_bias = tokens.mpass.iteration_depth_bias

            # --- alpha
            if tokens.mpass.alpha_rejection:
                self.alpha_rejection_function = tokens.mpass.alpha_rejection.function
                self.alpha_rejection_threshold = tokens.mpass.alpha_rejection.threshold

            if tokens.mpass.alpha_to_coverage:
                self.alpha_to_coverage = ' '.join(tokens.mpass.alpha_to_coverage)


            # --- objects
            if tokens.mpass.texture_units:
                for tu in tokens.mpass.texture_units:
                    self.texture_units.append( tu )

            if tokens.mpass.shaders:
                for sh in tokens.mpass.shaders:
                    self.shaders.append( sh )


    def __str__(self):
        repr = 'pass ' + self.name + '\n{\n'

        indent = '\t'

        repr += indent + 'ambient ' + str(self.ambient) + '\n'
        repr += indent + 'diffuse ' + str(self.diffuse) + '\n'
        repr += indent + 'emissive ' + str(self.emissive) + '\n'
        repr += indent + 'specular ' + str(self.specular) + ' ' + str(self.shininess) + '\n'

        for tu in self.texture_units:
            repr += str(tu)

        repr += '\n}\n'

        return repr

    # http://stackoverflow.com/questions/1436703/difference-between-str-and-repr-in-python
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

