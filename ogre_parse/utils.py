
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


def parse_script(aPath):

    res = None
    len_elems = 0
    scriptReader = ogre_parse.reader.ReadScript()
    with open(aPath, 'r') as f:
        script = f.read()
        try:
            res = scriptReader.parseString(script)
        except Exception as e:
            print('--an error occurred reading,\n%s with message:\n%s' % (aPath, str(e)))

    return res


def show_stats(aFolder):
    (mats, progs, comps) = script_search(aFolder)
    print('ogre statistics, under folder, %s, \nreading files: [%s] material, [%s] program, [%s] compositor' % (search_folder, len(mats), len(progs), len(comps)))

    len_mats = 0
    for m in mats:
        parsedres = parse_script(m)
        if not parsedres:
            continue

        script = parsedres[0]
        len_mats += len(script.materials)

        with open(m, 'r') as f:
            ftext = f.read()
            len_elems = ftext.count('material ')
            if len_elems != len(script.materials):
                print('!!! script file likely contains [%s] materials, but parser found [%s], in script: %s' % (len_elems, len(script.materials), m))
            else:
                print('parsed [%s] materials from file: %s' % (len(script.materials), m))

    len_progs = 0
    for p in progs:
        parsedres = parse_script(p)
        len_progs += len(parsedres[0].shaders)

    len_comps = 0
    for c in comps:
        parsedres = parse_script(c)
        len_comps += len(parsedres[0].compositors)

    print(20*'-' + '\n[%s] materials, [%s] shader definitions, [%s] compositors' % (len_mats, len_progs, len_comps))


if __name__ == '__main__':
    search_folder = 'D:\\Documents\\STI\\code\\projects\\SystemsTech\\SDK_various'
    # search_folder = r'C:\STISIM3'
    show_stats(search_folder)

    # fullpath = r'D:\Documents\STI\code\projects\SystemsTech\SDK_various\install\SystemsTech_SDK_rev1445\data\Examples\Particles\particles.material'
    # parsedres = parse_script(fullpath)
    # # print(parsedres.dump())
    # print(len(parsedres[0].materials))
    # # script = parsedres[0]
    # # print(str(script))

