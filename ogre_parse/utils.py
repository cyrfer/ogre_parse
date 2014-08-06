
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
    print('attempting to read: %s' % aPath)
    scriptReader = ogre_parse.reader.ReadScript()
    with open(aPath, 'r') as f:
        script = f.read()
        print('---- contents ----\n%s\n------ end -------' % script)
        try:
            res = scriptReader.parseString(script)
            print('[%s] elements in parsing results' % len(res))
        except:
            print('an error occurred reading: %s' % aPath)


def main():
    search_folder = 'D:\\Documents\\STI\\code\\projects\\SystemsTech\\SDK_various'
    (mats, progs, comps) = script_search(search_folder)
    print('ogre statistics, under folder, %s, \nreading files: [%s] material, [%s] program, [%s] compositor' % (search_folder, len(mats), len(progs), len(comps)))

    fullpath =  os.path.join(search_folder, 'data\\Examples\\TestScene\\cageCube.material')
    parse_script(fullpath)
    # for m in mats:
    #     parse_script(m)


if __name__ == '__main__':
    main()
