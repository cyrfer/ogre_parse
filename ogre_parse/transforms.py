__author__ = 'jgrant'

import copy
import logging

import ogre_parse.basemodel
import ogre_parse.submodel


# this will split Materials with a single-pass Technique into multiple passes
class SplitPass(object):
    def __init__(self):
        # can configure these
        self.split_iteration = 'once_per_light'

        self.shader_per_texture_vert_ambient = {0: 'phong',
                                                1: 'phong_1UV',
                                                2: 'phong_1UV'}

        # need to supply technique.scheme to get correct shader names
        self.shader_per_texture_frag_ambient = {          '': {0: 'BP',
                                                               1: 'BP_decal',
                                                               2: 'BP_decal_emissive'},
                                                'FR_stencil': {0: 'stencil_BP',
                                                               1: 'stencil_BP_decal',
                                                               2: 'stencil_BP_decal_emissive'}
                                                }

        # the default shaders if the pass does not use any
        self.shader_per_texture_vert = {0: 'phong',
                                        1: 'phong_1UV',
                                        2: 'phong_1UV_tangent',
                                        3: 'phong_1UV_tangent'}
                                        # 4: 'phong_1UV_tangent'} # should not need 4

        # need to supply technique.scheme to get correct shader names
        self.shader_per_texture_frag = {          '': {0: 'BP',
                                                       1: 'BP_decal',
                                                       2: 'BP_decal_normal',
                                                       3: 'BP_decal_normal_specular'},

                                        'FR_stencil': {0: 'stencil_BP',
                                                       1: 'stencil_BP_decal',
                                                       2: 'stencil_BP_decal_normal',
                                                       3: 'stencil_BP_decal_normal_specular'}
                                        }
                                        # 4: 'BP_decal_emissive_normal_specular'} # should not need 4

        # useful for filtering based on known problems with the resource
        self.has_bad_tangents = []

        # useful for correcting material color
        self.specular_gain = 0.01


    def log(self, msg, mname):
        logtext = 40*'*' + '\nMaterial [%s] had an issue: %s' % (mname, msg) + '\n' + 40*'*'
        logging.info(logtext)
        print(logtext)

    def add_shaders_direct(self, techscheme, p, mname):
        # self.log(10*'-' + 'adding shaders' + 10*'-', mname)

        sh_vert = ogre_parse.submodel.MShaderRef()
        sh_vert.stage = 'vertex_program_ref'
        sh_vert.resource_name = self.shader_per_texture_vert[len(p.texture_units)]

        sh_frag = ogre_parse.submodel.MShaderRef()
        sh_frag.stage = 'fragment_program_ref'

        if techscheme in self.shader_per_texture_frag:
            sh_frag.resource_name = self.shader_per_texture_frag[techscheme][len(p.texture_units)]
        else:
            self.log('add_shaders_direct: could not apply fragment shader for unknown Technique.scheme [%s]' % techscheme, mname)

        p.shaders.append( sh_vert )
        p.shaders.append( sh_frag )

    def add_shaders_ambient(self, techscheme, p, mname):
        # self.log(10*'-' + 'adding shaders' + 10*'-', mname)

        sh_vert = ogre_parse.submodel.MShaderRef()
        sh_vert.stage = 'vertex_program_ref'
        sh_vert.resource_name = self.shader_per_texture_vert_ambient[len(p.texture_units)]

        sh_frag = ogre_parse.submodel.MShaderRef()
        sh_frag.stage = 'fragment_program_ref'

        if techscheme in self.shader_per_texture_frag_ambient:
            sh_frag.resource_name = self.shader_per_texture_frag_ambient[techscheme][len(p.texture_units)]
        else:
            self.log('add_shaders_ambient: could not apply fragment shader for unknown Technique.scheme [%s]' % techscheme, mname)

        p.shaders.append( sh_vert )
        p.shaders.append( sh_frag )

    def split_pass(self, tech, mname):
        # assumes just a single pass exists
        if len(tech.passes) > 1:
            return

        pass0 = tech.passes[0] # the ambient pass

        if pass0.depth_write == 'off':
            pass0.depth_write = 'on'
            pass0.transparent_sorting = 'force'
            self.log('depth_write was [off], change to [on] and using [force] for transparent_sorting', mname)

        if pass0.lighting == 'off':
            self.log('lighting was disabled, enabling', mname)
            pass0.lighting = 'on'

        if pass0.shininess < 0.01:
            # fix shininess settings that don't work for lighting passes
            pass0.shininess = 20.0

        # we need to clear the shaders later, so no need for this anymore.
        # if len(pass0.shaders) < 2:
        #     pass0.shaders.clear() # sometimes a pass has just a frag shader
        #     self.add_shaders(pass0, mname)

        pass1 = copy.deepcopy(pass0)  # the per-light pass

        # adjust properties on new pass
        pass1.name = 'per_light'
        pass1.iteration = self.split_iteration
        pass1.illumination_stage = 'per_light'
        if pass1.scene_blend == 'one zero':
            pass1.scene_blend = 'add'
        # don't log these because they are known and common
        elif (pass1.scene_blend != 'src_alpha one_minus_src_alpha') or (pass1.scene_blend != 'alpha_blend'):
            pass1.scene_blend = 'src_alpha one'
        else:
            logtext = '''
----------------------------------------
  material [%s] is using scene_blend = [%s].
----------------------------------------''' % (mname, pass1.scene_blend)
            logging.info(logtext)
            print(logtext)

        pass1.depth_write = 'off'    # no need to overwrite
        pass1.depth_func = 'equal'   # better be the same, might help with flickering
        pass1.depth_check = 'on'     # on is default, but making sure here.

        # fix the shaders
        pass1.shaders.clear()
        if len(pass1.texture_units) == 4:  # sometimes the body has 4 textures by mistake (D,E,N,S)
            del pass1.texture_units[1]  # remove E, we only require D,N,S for this per-light pass

        # if len(pass1.texture_units) == 3:  # the DNS (body) material is messing up with 3 textures
        #     del pass1.texture_units[2:]  # only use 2 textures (D,N) instead of 3 (D,N,S)

        if len(pass1.texture_units) >= 2:  # (D,N,~S~)
            if mname in self.has_bad_tangents:
                self.log('removing [%s] texture_units because it was labelled to have bad tangent vectors' % (len(pass1.texture_units)-1), mname)
                del pass1.texture_units[1:]  # remove N,~S~, leaving only D

        self.add_shaders_direct(tech.scheme, pass1, mname)

        # turn OFF ambient
        pass1.ambient = ogre_parse.basemodel.Color(vals=[0, 0, 0, 1])
        pass1.emissive = ogre_parse.basemodel.Color(vals=[0, 0, 0, 1])

        # turn ON other colors
        pass1.diffuse = ogre_parse.basemodel.Color(vals=[1, 1, 1, 1])
        # specular is just too high
        pass1.specular = self.specular_gain * pass1.specular #ogre_parse.basemodel.Color(vals=[1, 1, 1, 1])
        if pass1.shininess < 0.01:
            # fix shininess settings that don't work for lighting passes
            pass1.shininess = 20.0

        # adjust properties on pass0
        pass0.name = 'ambient'
        pass0.iteration = 'once'
        pass0.illumination_stage = 'ambient'
        if pass0.scene_blend != 'one zero':
            if (pass0.scene_blend == 'alpha_blend') or (pass0.scene_blend == 'src_alpha one_minus_src_alpha'):
                pass
                # do not change, for now.
            else:
                self.log('needed to change pass0.scene_blend from [%s] to [%s]' % (pass0.scene_blend, 'one zero'), mname)
                pass0.scene_blend = 'one zero'

        # fix the shaders
        pass0.shaders.clear()
        if len(pass0.texture_units) == 4: # D,E,N,S
            del pass0.texture_units[2:] # we only require D,E
        elif len(pass0.texture_units) == 3: # D,N,S
            del pass0.texture_units[1:] # we only require D
        self.add_shaders_ambient(tech.scheme, pass0, mname)

        # turn ON ambient
        pass0.ambient = ogre_parse.basemodel.Color(vals=[1, 1, 1, 1])
        pass0.emissive = ogre_parse.basemodel.Color(vals=[0, 0, 0, 1])

        # turn OFF other colors
        pass0.diffuse = ogre_parse.basemodel.Color(vals=[0, 0, 0, 1])
        pass0.specular = ogre_parse.basemodel.Color(vals=[0, 0, 0, 1])

        # save the new pass
        tech.passes.append(pass1)

    # the required interface must return a material instance or None
    def mat(self, src):
        # grab the properties
        dest = copy.deepcopy(src)

        # split the passes in each Technique
        for itech in range(len(dest.techniques)):
            tdest = dest.techniques[itech]
            if len(tdest.passes) == 1:
                self.split_pass(tdest, dest.name)
            else:
                self.log('too many passes (%s) in Technique [%s]' % (len(tdest.passes), itech), src.name)
                continue

        return dest


# this operator merges 2 material techniques into 1
# that uses unified shaders instead of system-specific shaders.
class UnifyTechniques(object):
    def __init__(self):
        # a mapping of old shaders to new ones
        # the shaders that will be used to replace the old ones
        self.unified = {
                        # the vertex shaders
                        'phong_1UV_fog_tangent_ver120': 'phong_1UV_fog_tangent',
                        'phong_1UV_tangent_fog_hlsl': 'phong_1UV_fog_tangent',

                        # the pixel shaders
                        'BP_fog_decal_emissive_normal_specular_ver120': 'BP_fog_decal_emissive_normal_specular',
                        'BP_1UV_fog_decal_emissive_normal_specular_hlsl': 'BP_fog_decal_emissive_normal_specular',
                        'BP_fog_decal_normal_specular_ver120': 'BP_fog_decal_normal_specular',
                        'BP_1UV_fog_decal_normal_specular_hlsl': 'BP_fog_decal_normal_specular',
                        }

        # the default shaders if the pass does not use any
        self.shader_per_texture_vert = {0: 'phong',
                                        1: 'phong_1UV_fog',
                                        2: 'phong_1UV_fog_tangent',
                                        3: 'phong_1UV_fog_tangent',
                                        4: 'phong_1UV_fog_tangent'}
        self.shader_per_texture_frag = {0: 'BP_fog',
                                        1: 'BP_fog_decal',
                                        2: 'BP_fog_decal_normal',
                                        3: 'BP_fog_decal_normal_specular',
                                        4: 'BP_fog_decal_emissive_normal_specular'}

        # shaders that we don't need worry about
        self.ignore_list = ['phong_1UV_fog', 'stencil_BP_fog_decal', 'stencil_BP_fog_decal_emissive']

    def log(self, msg, mname):
        logtext = 'Unify Transform reports [%s] for Material [%s].' % (msg, mname)
        logging.info(logtext)
        print(logtext)

    def unify_pass(self, p, mname):
        # transform the shaders from non-unified names to unified names
        for sh in p.shaders:
            if sh.resource_name not in self.ignore_list:
                if sh.resource_name in self.unified:
                    # self.log('replacing shader [%s] with [%s]' % (sh.resource_name, self.unified[sh.resource_name]), mname)
                    sh.resource_name = self.unified[sh.resource_name]
                elif sh.resource_name in self.unified.values():
                    # self.log('already has unified shader [%s]' % sh.resource_name, mname)
                    pass
                else:
                    self.log(20*'-' + (' there are no unified matches for shader [%s] ' % sh.resource_name) + 20*'-', mname)

        if len(p.shaders) == 0:
            self.log(10*'-' + 'adding shaders' + 10*'-', mname)
            sh_vert = ogre_parse.submodel.MShaderRef()
            sh_vert.stage = 'vertex_program_ref'
            sh_vert.resource_name = self.shader_per_texture_vert[len(p.texture_units)]

            sh_frag = ogre_parse.submodel.MShaderRef()
            sh_frag.stage = 'fragment_program_ref'
            sh_frag.resource_name = self.shader_per_texture_frag[len(p.texture_units)]

            p.shaders.append(sh_vert)
            p.shaders.append(sh_frag)

    def unify_technique(self, tech, mname):
        for p in tech.passes:
            self.unify_pass(p, mname)

    def get_texture_names(self, tech):
        names = []
        for p in tech.passes:
            for tex in p.texture_units:
                names.append(tex.resource_name)

        return names

    def get_shader_names(self, tech):
        names = []
        for p in tech.passes:
            for sh in p.shaders:
                names.append(sh.resource_name)

        return names

    # find out if they are similar enough that they need to be merged
    def compare_techniques(self, t0, t1):
        if t0.scheme != t1.scheme:
            return False

        if len(t0.passes) != len(t1.passes):
            return False

        # grab all textures used
        # tex0 = [(x.resource_name for x in p.texture_units) for p in t0.passes]
        # tex1 = [(x.resource_name for x in p.texture_units) for p in t1.passes]
        tex0 = self.get_texture_names(t0)
        tex1 = self.get_texture_names(t1)
        tex0.sort()
        tex1.sort()

        # compare textures
        if tex0 != tex1:
            return False

        # grab all shaders used
        # sh0 = [(x.resource_name for x in p.shaders) for p in t0.passes]
        # sh1 = [(x.resource_name for x in p.shaders) for p in t1.passes]
        sh0 = self.get_shader_names(t0)
        sh1 = self.get_shader_names(t1)
        sh0.sort()
        sh1.sort()

        # compare shaders
        if sh0 != sh1:
            return False

        return True

    # the required interface must return a material instance or None
    def mat(self, src):
        # print(10*'-x' + ' doing Unify transformation on Material [%s].' % src.name)

        dest = copy.deepcopy(src)

        # replace non-unified shader names with unified ones
        for tdest in dest.techniques:
            self.unify_technique(tdest, src.name)

        if len(dest.techniques) > 1:
            # compare first techniques
            if self.compare_techniques(dest.techniques[0], dest.techniques[1]):
                self.log('consolidating techniques 0 and 1', dest.name)
                del dest.techniques[0]

        return dest

        # # check to see if this material needs merging
        # if len(src.techniques) < 2:
        #     # see if we can update the shaders
        #     if len(src.techniques) == 1:
        #         modded, ddest = self.unify_one(src)
        #         if modded:
        #             return ddest
        #
        #     self.bail('it did not have 2 Techniques', src.name)
        #     return None
        #
        # return self.unify_two(src)

