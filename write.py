#write.py

import datetime
import os
import pandas


def df_toCsv(dataframe, dictionary):
    #print(dataframe)

    output_filename = '_'.join((dictionary['files']['output_filename_csv'],dictionary['vars']['date']))
    output_filename = '.'.join((output_filename,dictionary['files']['output_extension_csv']))

    output_path = os.sep.join((dictionary['directories']['output_directory'], output_filename))
    print("Exporting file to : {}".format(output_path))
    dataframe.to_csv(output_path, index=False, encoding='utf-8-sig')

def df_toJson(dataframe, dictionary):
    #print(dataframe)

    output_filename = '_'.join((dictionary['files']['output_filename_json'], dictionary['vars']['date']))
    output_filename = '.'.join((output_filename, dictionary['files']['output_extension_json']))

    output_path = os.sep.join((dictionary['directories']['output_directory'], output_filename))
    print("Exporting file to : {}".format(output_path))
    dataframe.to_json(output_path)
