__author__ = 'jgrant'


from ogre_parse.basemodel import *

from pyparsing import ParseException
import math



# should be hooked up to a 'subreader.ReadTextureUnit' instance
class MTextureUnit(object):
    def __init__(self, tokens=None):
        self.name = ''
        self.resource_type = 'texture'
        self.resource_name = ''
        self.image_format = ''
        # self.cubic_images = {'front': '', 'back': '', 'left': '', 'right': '', 'up': '', 'down': ''}
        # self.cubic_address_mode = ''
        self.texture_alias = ''
        self.tex_coord_set = int(0)
        self.tex_address_mode = 'wrap'
        self.tex_border_colour = Color()
        self.filtering = 'linear linear point'
        self.scale = array.array('f', [1.0, 1.0])
        self.colour_op = 'modulate'
        self.colour_op_ex = ''
        self.colour_op_multipass_fallback = ''
        self.binding_type = 'fragment'
        self.env_map = 'off'
        self.indent = ''

        if tokens:
            tu = tokens.texture_unit

            if tu.name:
                self.name = tu.name

            if tu.required:
                # assume it is 'texture' until I support 'anim_texture' and 'cubic_texture'
                self.resource_type = tu.required.resource_type

                if tu.required.resource_properties:
                    if tu.required.resource_properties.name:
                        self.resource_name = tu.required.resource_properties.name

                    # an optional sub-property on the required property
                    if tu.required.resource_properties.format:
                        self.image_format = tu.required.resource_properties.format

                    # an optional sub-property on the required property
                    # if tu.required.resource_properties.type:
                    #     # should be one of: 1d, 2d, 3d, cubic
                    #     self.resource_texture_type = tu.required.resource_properties.type
                else:
                    # TODO: throw exception because the resource name is required.
                    pass

            if tu.texture_alias:
                self.texture_alias = tu.texture_alias[0]

            if tu.tex_coord_set:
                self.tex_coord_set = tu.tex_coord_set

            if tu.tex_address_mode:
                self.tex_address_mode = tu.tex_address_mode[0]

            if tu.tex_border_colour:
                self.tex_border_colour = tu.tex_border_colour

            if tu.filtering:
                self.filtering = ' '.join(tu.filtering[0])

            if tu.scale:
                self.scale[0] = tu.scale.x
                self.scale[1] = tu.scale.y

            if tu.colour_op:
                self.colour_op = tu.colour_op[0]

            if tu.colour_op_ex:
                # tu.colour_op_ex can contain mixed types, e.g. string and float
                # so we just store a string representation until there is a requirement to use
                # individual elements of the property.
                self.colour_op_ex = ' '.join(str(x) for x in tu.colour_op_ex[0].asList())

            if tu.colour_op_multipass_fallback:
                self.colour_op_multipass_fallback = ' '.join(tu.colour_op_multipass_fallback[0].asList())

            if tu.binding_type:
                self.binding_type = tu.binding_type[0]

            if tu.env_map:
                self.env_map = tu.env_map[0]



    def __str__(self):
        loc_indent = 4*' '
        repr = self.indent + 'texture_unit' + ((' ' + self.name) if self.name else '') + '\n{\n'

        if self.texture_alias:
            repr += self.indent + loc_indent + 'texture_alias ' + self.texture_alias + '\n'

        # check the resource type
        if self.resource_type == 'texture':
            repr += self.indent + loc_indent + self.resource_type + ' ' + self.resource_name +\
                    '\n'
                    # (self.resource_texture_type if (self.resource_texture_type!='2d') else '') +\
        elif self.resource_type == 'cubic_texture':
            pass
        elif self.resource_type == 'anim_texture':
            pass

        if self.tex_coord_set != int(0):
            repr += self.indent + loc_indent + 'tex_coord_set ' + str(self.tex_coord_set) + '\n'

        if self.tex_address_mode != 'wrap':
            repr += self.indent + loc_indent + 'tex_address_mode ' + self.tex_address_mode + '\n'

        if self.tex_border_colour != Color(vals=[0.0, 0.0, 0.0, 1.0]):
            repr += self.indent + loc_indent + 'tex_border_colour ' + str(self.tex_border_colour) + '\n'

        if (self.filtering != 'bilinear') and (self.filtering != 'linear linear point'):
            repr += self.indent + loc_indent + 'filtering ' + self.filtering + '\n'

        eps = 1e-7
        if (math.fabs(self.scale[0]-1.0) > eps) or (math.fabs(self.scale[1]-1.0) > eps):
            repr += self.indent + loc_indent + 'scale ' + str(self.scale[0]) + str(self.scale[1]) + '\n'

        if self.colour_op != 'modulate':
            repr += self.indent + loc_indent + 'colour_op' + self.colour_op + '\n'

        repr += self.indent + '}\n'

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

        self.indent = ''

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
                for k, val in shader.param_named_auto.items():
                    self.param_named_auto.update({k: ' '.join(val)})

            if shader.param_named:
                for k, val in shader.param_named.items():
                    self.param_named.update({k: ' '.join(val)})


    def __str__(self):
        loc_indent = 4*' '
        repr = ''

        repr += self.indent + self.stage + ' ' + self.resource_name + '\n{'

        # show all the 'auto' params
        for k,v in self.param_named_auto.items():
            repr += '\n' + self.indent + loc_indent + str(k) + ' ' + str(v)

        repr += '\n' + self.indent + '}\n'
        return repr

    # http://stackoverflow.com/questions/1436703/difference-between-str-and-repr-in-python
    __repr__ = __str__


# should be hooked up to a 'subreader.ReadPass' instance
class MPass(object):
    def __init__(self, tokens=None):
        self.name = ''

        # color
        self.ambient = Color(vals=[1, 1, 1, 1])
        self.diffuse = Color(vals=[1, 1, 1, 1])
        self.emissive = Color(vals=[0, 0, 0, 0])
        self.specular = Color(vals=[0, 0, 0, 0])
        self.shininess = float(0.0)

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

        # --- for text output formatting ---
        self.indent = ''

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
                self.specular = tokens.mpass.specular[0].color[0]
                self.shininess = tokens.mpass.specular[0].shininess[0]

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
        repr = self.indent + 'pass' + ((' ' + self.name) if self.name else '') + '\n' + self.indent + '{\n'

        loc_indent = 4*' '

        if self.ambient != Color(vals=[1, 1, 1, 1]):
            repr += self.indent + loc_indent + 'ambient ' + str(self.ambient) + '\n'

        if self.diffuse != Color(vals=[1, 1, 1, 1]):
            repr += self.indent + loc_indent + 'diffuse ' + str(self.diffuse) + '\n'

        if self.emissive != Color(vals=[0, 0, 0, 0]):
            repr += self.indent + loc_indent + 'emissive ' + str(self.emissive) + '\n'

        if (self.specular != Color(vals=[0, 0, 0, 0])) or (self.shininess != 0.0):
            repr += self.indent + loc_indent + 'specular ' + str(self.specular) + ' ' + str(self.shininess) + '\n'

        for tu in self.texture_units:
            tu.indent = self.indent + loc_indent
            repr += str(tu)

        repr += self.indent + '}'

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
        self.indent = ''

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
        loc_indent = 4*' '

        repr = ''
        repr += '\n' + self.indent + 'technique' + ((' ' + self.name) if self.name else '')
        repr += '\n' + self.indent + '{\n'

        if self.scheme:
            repr += '\n' + self.indent + loc_indent + 'scheme ' + self.scheme

        if self.lod_index != 0:
            repr += '\n' + self.indent + loc_indent + 'lod_index ' + str(self.lod_index)

        if self.shadow_caster_material:
            repr += '\n' + self.indent + loc_indent + 'shadow_caster_material ' + self.shadow_caster_material

        if self.shadow_receiver_material:
            repr += '\n' + self.indent + loc_indent + 'shadow_receiver_material ' + self.shadow_receiver_material

        for p in self.passes:
            p.indent = self.indent + loc_indent
            repr += str(p)

        repr += '\n' + self.indent + '}\n'

        return repr

    __repr__ = __str__

