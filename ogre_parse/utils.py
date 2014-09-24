
import glob
import os

import ogre_parse.reader

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


def parse_script(aPath, prefix=''):

    script = None
    scriptReader = ogre_parse.reader.ReadScript()
    with open(aPath, mode='r') as f:
        ftext = f.read()
        try:
            res = scriptReader.parseString(ftext)
            script = res.script
        except Exception as e:
            print('--an error occurred reading,\n%s with message:\n%s' % (aPath, str(e)))

    if prefix:
        fpath = os.path.join(prefix, os.path.split(aPath)[-1])
        if not os.path.isdir(os.path.dirname(fpath)):
            os.mkdir(os.path.dirname(fpath))

        if os.path.exists(fpath):
            print('--- overwriting existing file: %s' % fpath)
            # fpath = ' '.join(os.path.split(fpath)[0:-1]) + os.path.splitext(fpath)[-1]
            # print('--- renaming to avoid conflict with existing file: %s' % )

        print('writing to file: %s' % fpath)
        with open(fpath, mode='w') as f:
            f.write(str(script))

    return script


def show_stats(a_folder):
    (mats, progs, comps) = script_search(a_folder)
    print(20*'-' + '\nogre statistics, under folder, %s, \nreading files: [%s] material, [%s] program, [%s] compositor\n'
          % (search_folder, len(mats), len(progs), len(comps)) + 20*'-')

    len_mats = 0
    for m in mats:
        script = parse_script(m, 'forged_')
        if not script:
            continue

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

    print(20*'-' + '\n[%s] materials, [%s] shader definitions, [%s] compositors' % (len_mats, len_progs, len_comps))


if __name__ == '__main__':
    # search_folder = 'D:\\Documents\\STI\\code\\projects\\SystemsTech\\SDK_various'
    search_folder = r'C:\STISIM3\Data\Miscellaneous'
    show_stats(search_folder)

    # fullpath = r'D:\Documents\STI\code\projects\SystemsTech\SDK_various\install\SystemsTech_SDK_rev1445\data\Examples\Particles\particles.material'
    # parsedres = parse_script(fullpath)
    # # print(parsedres.dump())
    # print(len(parsedres[0].materials))
    # # script = parsedres[0]
    # # print(str(script))

