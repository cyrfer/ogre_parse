__author__ = 'jgrant'


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
        indent = '    '

        repr = '\n'
        repr += 'material ' + self.name
        repr += '\n{\n'

        if self.lod_strategy:
            repr += '\n' + indent + 'lod_strategy ' + self.lod_strategy

        if self.lod_values:
            repr += '\n' + indent + 'lod_values '
            for lod in self.lod_values:
                repr += lod

        if self.receive_shadows != 'on':
            repr += '\n' + indent + self.receive_shadows

        if self.transparency_casts_shadows != 'off':
            repr += '\n' + indent + self.transparency_casts_shadows

        for k,v in self.texture_alias.items():
            repr += '\n' + indent + k + ' ' + v

        for t in self.techniques:
            repr += t

        repr += '\n}\n'

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
            repr += m

        for s in self.shaders:
            repr += s

        for c in self.compositors:
            repr += c

    __repr__ = __str__


