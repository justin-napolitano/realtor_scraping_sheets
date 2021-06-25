#write.py

import datetime
from os import listdir
from os.path import isfile, join
import os


def df_toCsv(dictionary,file_name, dataframe,output_directory):
   #print(dataframe)
    output_filename = '_'.join((file_name, dictionary['universal_vars']['date']['date']))
    output_filename = '.'.join((output_filename, 'csv'))
    output_path = os.sep.join((output_directory, output_filename))
    print("Exporting file to : {}".format(output_path))

    dataframe.to_csv(output_path, index=False, encoding='utf-8-sig')

def df_toJson(dictionary,file_name, dataframe,output_directory):
    #print(dataframe)
    
    output_filename = '_'.join((file_name, dictionary['universal_vars']['date']['date']))
    output_filename = '.'.join((output_filename, 'json'))

    output_path = os.sep.join((output_directory, output_filename))
    print("Exporting file to : {}".format(output_path))
    dataframe.to_json(output_path)

def file_list(directory):
        mypath = directory
        #print(mypath)
        onlyfiles = [os.sep.join((mypath,f)) for f in listdir(mypath) if isfile(join(mypath, f))]
        
        print(onlyfiles)
        return onlyfiles




# r=root, d=directories, f = files
def file_list_walk(thisdir):
    onlyfiles = []
    for r, d, f in os.walk(thisdir):
        for file in f:
            if file.endswith(".json"):
                onlyfiles.append(os.path.join(r, file))
    return onlyfiles