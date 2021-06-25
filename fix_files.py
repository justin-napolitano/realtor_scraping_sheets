from os import listdir
from os.path import isfile, join
import os


def fix_files(dictionary):
    mypath = dictionary['tasks']['universal_vars']['directories']['to_merge']
    #print(mypath)
    #onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for f in listdir(mypath):
        remove = len(f)-9
        keep = 8 - remove
        print(remove)
        print(f[-remove:])
        move = remove -1
        print(f[-move:])
        number = f[-move:]
        name = 'data_'
        file_ext = '.json'
        filename = name + number + file_ext
        print(filename)
        path = os.sep.join((mypath,f))
        os.rename(path,filename)
        #print(f[:keep])
        

    #print(onlyfiles)\
    #print(len(onlyfiles))
    #onlyfiles.sort()
   # for f in onlyfiles:
   #     remove = len(f) - 9
   #     print(remove)
   #    print(f[-remove:])

    
    #for i in range(1,len(onlyfiles)):


