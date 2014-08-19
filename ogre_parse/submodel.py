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

        # show all the 'auto' params
        for k,v in self.param_named_auto.items():
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

        # light scissor
        self.light_scissor = 'off'
        self.light_clip_planes = 'off'

        # other
        self.illumination_stage = 'none'
        self.normalise_normals = 'off'
        self.transparent_sorting = 'on'

        # cull
        self.cull_hardware = 'clockwise'
        self.cull_software = 'back'

        # other
        self.lighting = 'on'
        self.shading = 'gouraud'
        self.polygon_mode = 'solid'
        self.polygon_mode_overrideable = 'true'
        self.fog_override = 'false'
        self.colour_write = 'on'
        self.start_light = int(0)
        self.max_lights = int(8)

        # iteration
        self.iteration = 'once'

        # points
        self.point_size = float(1.0)
        self.point_sprites = 'off'
        self.point_size_attenuation = 'off'
        self.point_size_min = float(0.0)
        self.point_size_max = float(1.0)


        # --- objects ---
        self.texture_units = []
        self.shaders = []

        # grab parsed results
        if tokens:
            if tokens.mpass.name:
                self.name = tokens.mpass.name

            # --- color
            if tokens.mpass.ambient:
                self.ambient = tokens.mpass.ambient[0]

            if tokens.mpass.diffuse:
                self.diffuse = tokens.mpass.diffuse[0]

            if tokens.mpass.emissive:
                self.emissive = tokens.mpass.emissive[0]

            if tokens.mpass.specular:
                # TODO: the parser should enabled child elements to be referred by name, not index.
                #  For example, specular.shininess, not [0][1].
                self.specular = tokens.mpass.specular[0][0]
                self.shininess = tokens.mpass.specular[0][1]

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

            # --- light scissor
            if tokens.mpass.light_scissor:
                self.light_scissor = ' '.join(tokens.mpass.light_scissor)

            if tokens.mpass.light_clip_planes:
                self.light_clip_planes = ' '.join(tokens.mpass.light_clip_planes)

            # --- other
            if tokens.mpass.illumination_stage:
                self.illumination_stage = ' '.join(tokens.mpass.illumination_stage)

            if tokens.mpass.normalise_normals:
                self.normalise_normals = ' '.join(tokens.mpass.normalise_normals)

            if tokens.mpass.transparent_sorting:
                self.transparent_sorting = ' '.join(tokens.mpass.transparent_sorting)

            # --- cull
            if tokens.mpass.cull_hardware:
                self.cull_hardware = ' '.join(tokens.mpass.cull_hardware)

            if tokens.mpass.cull_software:
                self.cull_software = ' '.join(tokens.mpass.cull_software)

            # --- other
            if tokens.mpass.lighting:
                self.lighting = ' '.join(tokens.mpass.lighting)

            if tokens.mpass.shading:
                self.shading = ' '.join(tokens.mpass.shading)

            if tokens.mpass.polygon_mode:
                self.polygon_mode = ' '.join(tokens.mpass.polygon_mode)

            if tokens.mpass.polygon_mode_overrideable:
                self.polygon_mode_overrideable = ' '.join(tokens.mpass.polygon_mode_overrideable)

            if tokens.mpass.fog_override:
                self.fog_override = ' '.join(tokens.mpass.fog_override)

            if tokens.mpass.colour_write:
                self.colour_write = ' '.join(tokens.mpass.colour_write)

            if tokens.mpass.start_light:
                self.start_light = tokens.mpass.start_light[0]

            if tokens.mpass.max_lights:
                self.max_lights = tokens.mpass.max_lights[0]

            if tokens.mpass.iteration:
                self.iteration = ' '.join(tokens.mpass.iteration)

            # --- point
            if tokens.mpass.point_size:
                self.point_size = tokens.mpass.point_size[0]

            if tokens.mpass.point_sprites:
                self.point_sprites = ' '.join(tokens.mpass.point_sprites)

            if tokens.mpass.point_size_attenuation:
                self.point_size_attenuation = ' '.join(tokens.mpass.point_size_attenuation)

            if tokens.mpass.point_size_min:
                self.point_size_min = tokens.mpass.point_size_min[0]

            if tokens.mpass.point_size_max:
                self.point_size_max = tokens.mpass.point_size_max[0]


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


# should be hooked up to a 'subreader.ReadTechnique' instance
class MTechnique(object):
    def __init__(self, tokens=None):
        self.name = ''
        self.scheme = ''
        self.lod_index = int(0)
        self.shadow_caster_material = ''
        self.shadow_receiver_material = ''
        self.gpu_vendor_rule = []
        self.gpu_device_rule = []
        self.passes = []

        if tokens:
            tech = tokens.technique

            if tech.name:
                self.name = tech.name

            if tech.scheme:
                self.scheme = ' '.join(tech.scheme)

            if tech.lod_index:
                self.lod_index = tech.lod_index[0]

            if tech.shadow_caster_material:
                self.shadow_caster_material = ' '.join(tech.shadow_caster_material)

            if tech.shadow_receiver_material:
                self.shadow_receiver_material = ' '.join(tech.shadow_receiver_material)

            if tech.gpu_vendor_rules:
                for vr in tech.gpu_vendor_rules:
                    self.gpu_vendor_rule.append( vr )

            if tech.gpu_device_rules:
                for dr in tech.gpu_device_rules:
                    self.gpu_device_rule.append( dr )

            if tech.passes:
                for p in tech.passes:
                    self.passes.append( p )


    def __str__(self):
        indent = '    '

        repr = ''
        repr += '\n' + indent + 'technique ' + self.name
        repr += '\n' + indent + '{\n'

        if self.scheme:
            repr += '\n' + 2*indent + 'scheme ' + self.scheme

        if self.lod_index != 0:
            repr += '\n' + 2*indent + 'lod_index ' + str(self.lod_index)

        if self.shadow_caster_material:
            repr += '\n' + 2*indent + 'shadow_caster_material ' + self.shadow_caster_material

        if self.shadow_receiver_material:
            repr += '\n' + 2*indent + 'shadow_receiver_material ' + self.shadow_receiver_material

        repr += '\n' + indent + '}\n'

        return repr

    __repr__ = __str__

