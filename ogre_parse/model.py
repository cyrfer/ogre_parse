__author__ = 'jgrant'




# TODO: make a member for each property in:
# http://www.ogre3d.org/docs/manual/manual_17.html#Texture-Units
class TextureUnit(object):
    def __init__(self, parsed=None):
        # as a shortcut from named members, use a dictionary
        # TODO: define these names and default values
        self.properties = {}

        # initialize from the parse results if available
        if parsed:
            print('TextureUnit parsed: %s' % parsed)
            print('results name = %s' % parsed[0].getName())
            for k,v in parsed[0].items():
                print('TextureUnit: update( {%s:%s} )' % (k,v))
                self.properties.update( {k:v})

    # return the property stored in the dictionary
    def get(self, prop_name):
        return self.properties[prop_name]


# TODO: model the properties of:
# http://www.ogre3d.org/docs/manual/manual_23.html#Using-Vertex_002fGeometry_002fFragment-Programs-in-a-Pass
class ShaderRef(object):
    def __init__(self):
        # TODO: define these names and default values
        self.properties = {}

# TODO: model the properties of:
# http://www.ogre3d.org/docs/manual/manual_16.html#Passes
class Pass(object):
    def __init__(self):
        self.textures = []
        self.shaders = []

        # TODO: define these names and default values
        self.properties = {}

# TODO: model the properties of:
# http://www.ogre3d.org/docs/manual/manual_15.html#Techniques
class Technique(object):
    def __init__(self):
        self.passes = []

        # TODO: define these names and default values
        self.properties = {}

# TODO: model the properties of:
# http://www.ogre3d.org/docs/manual/manual_14.html#Material-Scripts
class Material(object):
    def __init__(self):
        self.techniques = []

        # TODO: define these names and default values
        self.properties = {}



