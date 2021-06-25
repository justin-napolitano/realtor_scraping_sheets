#load_vars.py
import os
import datetime
import yaml
import glob
import datetime
from pprint import pprint

def load_config():
    #print("test")
    stream = open("config.yaml", 'r')
    task_dictionary = yaml.load(stream)
    return task_dictionary


def set_environmental_vars(dictionary):
    dictionary['environmental_vars']['directories']['cwd'] = os.getcwd()
    dictionary['environmental_vars']['sep'] = os.sep
    dictionary['environmental_vars']['directories']['to_merge'] = dictionary['environmental_vars']['sep'].join((dictionary['environmental_vars']['directories']['cwd'],dictionary['environmental_vars']['directories']['to_merge']))
    dictionary['environmental_vars']['directories']['merged_data'] = dictionary['environmental_vars']['sep'].join((dictionary['environmental_vars']['directories']['cwd'],dictionary['environmental_vars']['directories']['merged_data']))
    dictionary['environmental_vars']['directories']['log_directory'] = dictionary['environmental_vars']['sep'].join((dictionary['environmental_vars']['directories']['cwd'],dictionary['environmental_vars']['directories']['log_directory']))
    dictionary['environmental_vars']['directories']['extracted_data'] = dictionary['environmental_vars']['sep'].join((dictionary['environmental_vars']['directories']['cwd'],dictionary['environmental_vars']['directories']['extracted_data']))
    dictionary['environmental_vars']['directories']['mapped_data'] = dictionary['environmental_vars']['sep'].join((dictionary['environmental_vars']['directories']['cwd'],dictionary['environmental_vars']['directories']['mapped_data']))
    dictionary['environmental_vars']['date']['date'] = str(datetime.date.today())
    dictionary['environmental_vars']['date']['datetime'] = str(datetime.datetime.now())
    dictionary['environmental_vars']['directories']['cities'] = dictionary['environmental_vars']['sep'].join((dictionary['environmental_vars']['directories']['cwd'],dictionary['environmental_vars']['directories']['cities']))
    dictionary['environmental_vars']['directories']['dnn'] = dictionary['environmental_vars']['sep'].join((dictionary['environmental_vars']['directories']['cwd'],dictionary['environmental_vars']['directories']['dnn']))
    
    return True

def load_files(dictionary):
    os.chdir(dictionary['directories']['input_directory'])
    dictionary['files']['files_to_merge'] = [i for i in glob.glob('*.{}'.format(dictionary['files']['input_extension']))]
    os.chdir(dictionary['directories']['cwd'])
    return True

def load_date(dictionary):
    dictionary['vars']['date'] = str(datetime.date.today())
    dictionary['vars']['datetime']=str(datetime.datetime.now())
    return True

def batchify(dictionary,batch):
    for k,v  in dictionary.items():
        for sheet in v['sheets']:
            #pprint(sheet['properties']['gridProperties']['rowCount'])
            number = sheet['properties']['gridProperties']['rowCount']
            sheet['properties']['end_column'] = colnum_string(sheet['properties']['gridProperties']['columnCount'])
            sheet['properties']['divmod'] = divmod(number,batch)
            sheet['properties']['batches'] = batch_ranges(batch,sheet['properties']['divmod'])
            sheet['properties']['ranges'] = generate_search_ranges(sheet['properties'])
    
            #print(divmod(number,batch))


def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def batch_ranges(batch_size,divymod):
    start = 0
    start_end = {'start': 0, 'end': 0}
    end = 0
    batches = {}
    rge = range(divymod[0]+1)
    #print(rge(stop))

    for batch in rge:
        
        if batch == 0 and batch == divymod[0]:
            print("zer0 and divymod case")
            start_end['start'] = 2
            start_end['end'] = divymod[1]
            batches[str(batch)] = start_end.copy()
        
        elif batch == 0 and batch != divymod[0]:
            print('zero and not divy case')
            start_end['start'] = 2
            start_end['end'] = batch_size
            batches[str(batch)] = start_end.copy()
        
        
        elif batch == divymod[0]:
            start_end['start'] = (batch * batch_size) + 1
            start_end['end'] = (batch * batch_size) + divymod[1]
            batches[str(batch)] = start_end.copy()
        
        else :
            start_end['start'] = (batch * batch_size) + 1
            start_end['end'] = (batch * batch_size) + batch_size
            batches[str(batch)] = start_end.copy()

    return batches



def generate_search_ranges(sheet_properties):
    title = "'{}'".format(sheet_properties['title'])
    title = title + "!"
    #title = "'{}'".format(title)
    
    ranges = {}
    #header = title + "A" + str(1) + ":" + sheet_properties['end_column'] + str(1)
    ranges['header'] = title + "A" + str(1) + ":" + sheet_properties['end_column'] + str(1)
    #print(sheet_properties['batches'])
    for k,value in sheet_properties['batches'].items():
        rge = title + "A" + str(value['start']) + ":" + sheet_properties['end_column'] + str(value['end'])
        #print(rge)
        ranges[k] = rge
    




    return ranges

        

#print(colnum_string(28))
        


