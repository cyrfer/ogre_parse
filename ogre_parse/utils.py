
import os


import ogre_parse.reader
from ogre_parse.transforms import *


# collect all files with an extension matching on of 'extensions'
# returns (materials, programs, compositors)
def script_search(aFolder):
    mats = []
    progs = []
    comps = []

    for root, dirs, files in os.walk(aFolder):
        for file in files:
            if file.endswith('.material'):
                mats.append( os.path.join(root, file))
            elif file.endswith('.program'):
                progs.append( os.path.join(root, file))
            elif file.endswith('.compositor'):
                comps.append( os.path.join(root, file))

    return (mats, progs, comps)


def transform_script(input_script, fpath, oper):
    output_script = ogre_parse.model.Script()

    # change all the materials with our operator
    for m in input_script.materials:
        mt = oper.mat(m)
        if mt:
            output_script.materials.append(mt)
        else:
            output_script.materials.append(m)

    return output_script


def parse_script(aPath):

    script = None
    scriptReader = ogre_parse.reader.ReadScript()
    with open(aPath, mode='r') as f:
        print('reading file: %s' % aPath)
        ftext = f.read()
        try:
            res = scriptReader.parseString(ftext)
            script = res.script
        except Exception as e:
            print('--an error occurred reading,\n%s with message:\n%s' % (aPath, str(e)))

    return script


def count_passes_with_no_shaders(mlist):
    cns = 0
    for m in mlist:
        for t in m.techniques:
            for p in t.passes:
                if len(p.shaders) == 0:
                    cns += 1
                    print('material [%s] has no shaders in a pass' % m.name)

    return cns


def show_stats(a_folder):
    (mats, progs, comps) = script_search(a_folder)
    print(20*'-' + '\nogre statistics, under folder, %s, \nreading files: [%s] material, [%s] program, [%s] compositor\n'
          % (search_folder, len(mats), len(progs), len(comps)) + 20*'-')

    # prefix = 'forged_' # needed for vehicles, modified parser to read and write reversed order for texture-shader-order bug. allowed me to see any diffs easily.
    # prefix = 'fixed_'  # needed for vehicles, changed order of Vehicles' textures and shaders.
    # prefix = 'unified_' # folder to hold results of the UnifyTechniques transform
    prefix = 'multipass_' # folder to hold the results of the SplitPass transform
    passes_with_no_shaders = 0
    len_mats = 0
    for m in mats:
        script = parse_script(m)
        if not script:
            continue
        else:
            if prefix:
                fpath = os.path.join(prefix, os.path.split(m)[-1])
                if not os.path.isdir(os.path.dirname(fpath)):
                    os.mkdir(os.path.dirname(fpath))

                if os.path.exists(fpath):
                    print('--- overwriting existing file: %s' % fpath)
                    # fpath = ' '.join(os.path.split(fpath)[0:-1]) + os.path.splitext(fpath)[-1]
                    # print('--- renaming to avoid conflict with existing file: %s' % )

                # output_script = transform_script(script, fpath, UnifyTechniques())
                output_script = transform_script(script, fpath, SplitPass())

                print('writing to file: %s' % fpath)
                with open(fpath, mode='w') as f:
                    f.write(str(output_script))

                script = output_script

        passes_with_no_shaders += count_passes_with_no_shaders(script.materials)
        len_mats += len(script.materials)

        with open(m, 'r') as f:
            ftext = f.read()
            len_elems = ftext.count('material ')
            if len_elems != len(script.materials):
                print('!!! script file likely contains [%s] materials, but parser found [%s], in script: %s'
                      % (len_elems, len(script.materials), m))
            else:
                print('parsed [%s] materials from file: %s' % (len(script.materials), m))

    len_progs = 0
    for p in progs:
        script = parse_script(p)
        if not script:
            continue

        len_progs += len(script.shaders)

    len_comps = 0
    for c in comps:
        script = parse_script(c)
        if not script:
            continue

        len_comps += len(script.compositors)

    print(20*'-' + '\n[%s] materials ([%s] passes with no shaders), [%s] shader definitions, [%s] compositors' \
          % (len_mats, passes_with_no_shaders, len_progs, len_comps))


if __name__ == '__main__':
    # search_folder = r'original'
    # search_folder = r'fixed_'
    search_folder = r'unified_'
    show_stats(search_folder)

