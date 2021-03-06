__author__ = 'jgrant'


# hook this up to a ogre_parse.reader.ReadShaderDeclaration
class ShaderDeclaration(object):
    def __init__(self, tokens=None):
        self.stage = ''     # vertex_program
        self.name = ''      # myVertShader
        self.language = ''  # hlsl or glsl
        self.source = ''    # cloud.hlsl
        self.entry_point = ''   # CloudVS
        self.target = ''    # vs_2_0

        self.has_default_params = False
        self.param_named_auto = {}  # param_named_auto Mv view_matrix
        self.param_named = {}  # param_named_auto Mv view_matrix


        if tokens and tokens.shader:
            sh = tokens.shader

            if sh.stage:
                self.stage = sh.stage

            if sh.name:
                self.name = sh.name

            if sh.language:
                self.language = sh.language

            if sh.source:
                self.source = sh.source[0]

            if sh.entry_point:
                self.entry_point = sh.entry_point[0]

            if sh.target:
                self.target = sh.target[0]

            if sh.default_params:
                if sh.default_params.param_named_auto:
                    for k, val in sh.default_params.param_named_auto:
                        self.param_named_auto.update({k: ' '.join(val)})

                if sh.default_params.param_named:
                    for k, val in sh.default_params.param_named:
                        self.param_named.update({k: ' '.join(val)})

                if self.param_named_auto or self.param_named:
                    self.has_default_params = True


    def __str__(self):
        loc_indent = 4*' '

        repr = ''
        repr += '\n' + self.stage + ' ' + self.name + ' ' + self.language
        repr += '\n' + '{'
        repr += '\n' + loc_indent + 'source ' + self.source

        if self.language == 'hlsl':
            repr += '\n' + loc_indent + 'entry_point ' + self.entry_point
            repr += '\n' + loc_indent + 'target ' + self.target

        # --- default_params --- #
        repr += 2*'\n' + loc_indent + 'default_params'
        repr += '\n' + loc_indent + '{'

        for k, v in self.param_named_auto.items():
            repr += '\n' + 2*loc_indent + 'param_named_auto ' + k + ' ' + v

        for k, v in self.param_named.items():
            repr += '\n' + 2*loc_indent + 'param_named ' + k + ' ' + v

        repr += '\n' + loc_indent + '}'
        # --- end default_params --- #

        repr += '\n' + '}'

        return repr

    __repr__ = __str__


# hook this up to a ogre_parse.reader.ReadMaterial
# models the properties of:
# http://www.ogre3d.org/docs/manual/manual_14.html#Material-Scripts
class Material(object):
    def __init__(self, tokens=None):
        self.name = ''
        self.lod_strategy = 'Distance'
        self.lod_values = []
        self.receive_shadows = 'on'
        self.transparency_casts_shadows = 'off'
        self.texture_alias = {}
        self.techniques = []

        if tokens:
            mat = tokens.material
            if mat.name:
                self.name = mat.name

            if mat.lod_strategy:
                self.lod_strategy = ' '.join(mat.lod_strategy)

            if mat.lod_values:
                for lod in mat.lod_values:
                    self.lod_values.append(lod)

            if mat.receive_shadows:
                self.receive_shadows = ' '.join(mat.receive_shadows)

            if mat.transparency_casts_shadows:
                self.transparency_casts_shadows = ' '.join(mat.transparency_casts_shadows)

            if mat.texture_alias:
                for k, v in mat.texture_alias.items():
                    self.texture_alias.update({k: v})

            if mat.techniques:
                for t in mat.techniques:
                    self.techniques.append(t)


    def __str__(self):
        loc_indent = 4*' '

        repr = '\n'
        repr += 'material ' + self.name
        repr += '\n{'

        if self.lod_strategy != 'Distance':
            repr += '\n' + loc_indent + 'lod_strategy ' + self.lod_strategy

        if self.lod_values:
            repr += '\n' + loc_indent + 'lod_values '
            for lod in self.lod_values:
                repr += ' ' + str(lod)

        if self.receive_shadows != 'on':
            repr += '\n' + loc_indent + self.receive_shadows

        if self.transparency_casts_shadows != 'off':
            repr += '\n' + loc_indent + self.transparency_casts_shadows

        for k, v in self.texture_alias.items():
            repr += '\n' + loc_indent + k + ' ' + v

        for ti in range(len(self.techniques)):
            t = self.techniques[ti]
            t.indent = loc_indent
            repr += str(t) + ('\n' if (ti < (len(self.techniques)-1)) else '')

        repr += '\n' + '}\n'

        return repr

    __repr__ = __str__


# hook this up to a 'ogre_parse.reader.ReadCompositor' instance.
class Compositor(object):
    def __init__(self, tokens):
        self.name = ''

        if tokens:
            c = tokens.compositor

            if c.name:
                self.name = c.name

    def __str__(self):
        repr += '\n' + 'compositor ' + self.name
        repr += '\n' + '{'
        repr += '\n' + '}'
        return repr

    __repr__ = __str__


# hook this up to an 'ogre_reader.reader.ReaderScript' instance.
class Script(object):
    def __init__(self, tokens=None):
        self.materials = []
        self.shaders = []
        self.compositors = []

        if tokens:
            for t in tokens:
                if isinstance(t, Material):
                    self.materials.append(t)
                    # print('added a material to the script!')

                elif isinstance(t, ShaderDeclaration):
                    self.shaders.append(t)
                    # print('added a shader to the script!')

                elif isinstance(t, Compositor):
                    self.shaders.append(t)
                    # print('added a compositor to the script!')


    def __str__(self):
        repr = ''

        for m in self.materials:
            repr += str(m)
            repr += '\n'

        for s in self.shaders:
            repr += str(s)

        for c in self.compositors:
            repr += str(c)

        return repr

    __repr__ = __str__

