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


    def __str__(self):
        loc_indent = 4*'-'

        repr = ''
        repr += '\n' + self.stage + ' ' + self.name + self.language
        repr += '\n' + '{'
        repr += '\n' + loc_indent + 'source ' + self.source
        repr += '\n' + loc_indent + 'entry_point ' + self.entry_point
        repr += '\n' + loc_indent + 'target ' + self.target
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
                repr += lod

        if self.receive_shadows != 'on':
            repr += '\n' + loc_indent + self.receive_shadows

        if self.transparency_casts_shadows != 'off':
            repr += '\n' + loc_indent + self.transparency_casts_shadows

        for k,v in self.texture_alias.items():
            repr += '\n' + loc_indent + k + ' ' + v

        for t in self.techniques:
            t.indent = loc_indent
            repr += str(t)

        repr += '}\n'

        return repr

    __repr__ = __str__


# hook this up to an 'ogre_reader.reader.ReaderScript' instance.
class Script(object):
    def __init__(self, tokens=None):
        self.materials = []
        self.shaders = []
        self.compositors = []

        if tokens:
            if tokens.materials:
                for m in tokens.materials:
                    self.materials.append(m)

            if tokens.shaders:
                for s in tokens.shaders:
                    self.shaders.append(s)

            if tokens.compositors:
                for c in tokens.compositors:
                    self.compositors.append(c)


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


