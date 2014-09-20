__author__ = 'cyrfer'

# This file defines 'readers' for the major classes of OGRE objects, including:
# - materials
# - shader declarations
# - compositors

# OGRE permits putting any of the major classes into any of the OGRE resource file types, including:
# - .material
# - .program
# - .compositor

# Because any script may define any of the definitions, a catch-all "script reader" is defined here.


from ogre_parse.basereader import *
import ogre_parse.subreader
from ogre_parse.model import *

# grammar to parse materials
class ReadMaterial(ReadBase):
    def __init__(self):
        technique_ = ogre_parse.subreader.ReadTechnique()

        # --- define the material parser
        lod_strategy = Group(Keyword('lod_strategy').suppress() + ident)('lod_strategy')
        lod_values = Group(Keyword('lod_values').suppress() + OneOrMore(integer))('lod_values')
        receive_shadows = Group(Keyword('receive_shadows').suppress() + onoff_val_spec)('receive_shadows')
        transparency_casts_shadows = Group(Keyword('transparency_casts_shadows').suppress() + onoff_val_spec)('transparency_casts_shadows')
        set_texture_alias_key = Keyword('set_texture_alias').suppress() + identspec
        set_texture_alias_val = identspec

        matDecl = Keyword('material').suppress() + ident('name') + \
                    lbrace + \
                        Optional(lod_strategy) + \
                        Optional(lod_values) + \
                        Optional(receive_shadows) + \
                        Optional(transparency_casts_shadows) + \
                        dictOf(set_texture_alias_key, set_texture_alias_val)('texture_alias') + \
                        OneOrMore( technique_.getGrammar() )('techniques') + \
                    rbrace
        material_ = Group(matDecl)('material')
        material_.setParseAction(Material)
        super(ReadMaterial, self).__init__(material_)


# grammar to parse shader declarations
class ReadShaderDeclaration(ReadBase):
    def __init__(self):

        param_named_auto_spec = Keyword('param_named_auto').suppress() + ident
        param_named_spec = Keyword('param_named').suppress() + ident

        default_params = Group( Keyword('default_params').suppress() + \
                                lbrace + \
                                    dictOf( param_named_auto_spec, propList )('param_named_auto') + \
                                    dictOf( param_named_spec,      propList )('param_named') + \
                                rbrace \
                               )('default_params')

        # shaderDeclPropName = oneOf('source entry_point target delegate')
        # shaderDeclProp = Group(shaderDeclPropName + propList)
        shaderStage = oneOf('vertex_program geometry_program fragment_program')('stage')
        shaderName = ident('name')
        shaderLang = oneOf('glsl hlsl cg asm')('language')

        source = Group(Keyword('source').suppress() + identspec)('source')
        entry_point = Group(Keyword('entry_point').suppress() + identspec)('entry_point')
        target = Group(Keyword('target').suppress() + identspec)('target')

        hlsl = ( \
                    source & \
                    entry_point & \
                    target \
                )

        glsl = ( \
                    source \
                )

        shaderDeclDecl = shaderStage + shaderName + shaderLang + \
                            lbrace + \
                            (\
                                (hlsl | glsl) & \
                                Optional(default_params) \
                            ) + \
                            rbrace
                                # (shaderDeclProps_unified | shaderDeclProps_hlsl | shaderDeclProps_glsl | shaderDeclProps_cg | shaderDeclProps_asm)
        shader_declaration = Group(shaderDeclDecl)('shader')
        shader_declaration.setParseAction(ShaderDeclaration)
        super(ReadShaderDeclaration, self).__init__(shader_declaration)


# grammar to parse compositors
class ReadCompositor(ReadBase):
    def __init__(self):
        compTexture = Group(Keyword('texture') + OneOrMore(ident))
        compTargetPropName = oneOf('input only_initial visibility_mask load_bias material_scheme shadows pass')
        compTargetProp = Group(compTargetPropName)
        compTarget = Group(Keyword('target') + ident + lbrace + ZeroOrMore(compTargetProp) + rbrace)
        compOutput = Group(Keyword('target_output') + lbrace + ZeroOrMore(compTargetProp) + rbrace)
        compTech = Group(Keyword('technique').suppress() + \
                    lbrace + \
                        ZeroOrMore(compTexture) + \
                        ZeroOrMore(compTarget) + \
                        compOutput + \
                    rbrace)

        compDecl = Keyword('compositor').suppress() + ident + \
                    lbrace + \
                        OneOrMore(compTech) + \
                    rbrace

        compositor = Group(compDecl)
        super(ReadCompositor, self).__init__(compositor)


# grammar to parse anything in an ogre script (.material, .compositor, .program)
class ReadScript(ReadBase):
    def __init__(self):
        material_ = ReadMaterial().getGrammar()
        shader_declaration_ = ReadShaderDeclaration().getGrammar()
        compositor_ = ReadCompositor().getGrammar()

        resourceType = material_ | compositor_ | shader_declaration_

        scriptDecl = ZeroOrMore(resourceType)
        scriptDecl.setParseAction(Script)

        super(ReadScript, self).__init__(scriptDecl('script'))

    def getGrammar(self):
        return self.grammar_

