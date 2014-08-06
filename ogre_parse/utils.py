
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

    len_elems = 0
    scriptReader = ogre_parse.reader.ReadScript()
    with open(aPath, 'r') as f:
        script = f.read()
        # print('---- contents ----\n%s\n------ end -------' % script)
        try:
            res = scriptReader.parseString(script)
            len_elems = len(res)
            print('[%s] elements in file: %s' % (len_elems, aPath))
        except:
            print('--an error occurred reading: %s' % aPath)

    return len_elems


def show_stats(aFolder):
    (mats, progs, comps) = script_search(search_folder)
    print('ogre statistics, under folder, %s, \nreading files: [%s] material, [%s] program, [%s] compositor' % (search_folder, len(mats), len(progs), len(comps)))

    len_mats = 0
    for m in mats:
        len_mats += parse_script(m)

    len_progs = 0
    for p in progs:
        len_progs += parse_script(p)

    len_comps = 0
    for c in comps:
        len_comps += parse_script(c)

    print('[%s] materials, [%s] shader definitions, [%s] compositors' % (len_mats, len_progs, len_comps))

    # fullpath = r'D:\Documents\STI\code\projects\SystemsTech\SDK_various\data\Examples\Agent\cargo\exports\cargo.material'
    # parse_script(fullpath)


if __name__ == '__main__':
    search_folder = 'D:\\Documents\\STI\\code\\projects\\SystemsTech\\SDK_various'
    show_stats(search_folder)
