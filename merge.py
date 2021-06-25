#merge.py

# batch_merge.py
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

import os
import glob
import pandas as pd
import datetime
import json
import urllib.request




def batch_merge(dictionary: dict):
    
    input_directory = dictionary['directories']['input_directory']
    #output_directory = cwd + dictionary['output_directory']
    os.chdir(dictionary['directories']['input_directory'])
    print("Reading Files From : {}".format(input_directory))

    #getting files from directory
    files_to_merge = dictionary['files']['files_to_merge']

    print("Files to Merge: {}".format(files_to_merge))
    #combine all files in the list
 
    master_chunksize = dictionary['vars']['master_chunksize']
    chunksize = master_chunksize
    extra_chunk = None # Initialize the extra chunk.
    
    for file in files_to_merge:
        csv_file = file

        # Alter chunksize if extra chunk is not None.
        if extra_chunk is not None:
            chunksize = master_chunksize - extra_chunk.shape[0]

        for chunk in pd.read_csv(csv_file, chunksize=chunksize):
            if extra_chunk is not None: 
                # Concatenate last small chunk of previous file with altered first chunk of next file.
                chunk = pd.concat([chunk, extra_chunk], sort=True)
                extra_chunk = None
                chunksize = master_chunksize # Reset chunksize.
            elif chunk.shape[0] < chunksize:
                # If last chunk is less than chunk size, set is as the extra bit.
                extra_chunk = chunk
                break

            yield chunk
    os.chdir(dictionary['directories']['cwd'])



def merge_zip_data(lst: list):
    #dumb_merge = pd.DataFrame()
    data_merged = pd.DataFrame()
    could_not_merge = 0 
    for f in lst:
        try:
            data_merged = data_merged.append(pd.read_csv(f),ignore_index = True)
    #        #print(pd.read_json(f))
    #        df=pd.read_json(f)
    #        agent_data_tmp = df.props.pageProps['pageData']['agents']
    #        agent_data_merged = pd.append(agent_data_tmp)
    #        #dumb_merge= dumb_merge.append(pd.read_json(f),ignore_index = True)
        except:
            print('could not append file {}'.format(f))
            could_not_merge +=1
            pass
    #print (could_not_merge)
    return data_merged

def merge_agent_data(lst: list):
    #dumb_merge = pd.DataFrame()
    agent_data_merged = pd.DataFrame()
    could_not_merge = 0 
    for f in lst:
        try:
            agent_data_merged = agent_data_merged.append(pd.read_json(f).props.pageProps['pageData']['agents'],ignore_index = True)
    #        #print(pd.read_json(f))
    #        df=pd.read_json(f)
    #        agent_data_tmp = df.props.pageProps['pageData']['agents']
    #        agent_data_merged = pd.append(agent_data_tmp)
    #        #dumb_merge= dumb_merge.append(pd.read_json(f),ignore_index = True)
        except:
            print('could not append file {}'.format(f))
            could_not_merge +=1
            pass
    #print (could_not_merge)
    return agent_data_merged

def merge_json(lst: list):
    #dumb_merge = pd.DataFrame()
    
    #lst.remove('/Users/justinnapolitano/Dropbox/python/Projects/webscraping/realtor.com/merged_data/.DS_Store')
    merged_json_data = pd.DataFrame()
    could_not_merge = 0 
    for f in lst:
        #print(pd.read_json(f))
        try:
            #print(f)
            #print(pd.read_json(f))
            merged_json_data = merged_json_data.append(pd.read_json(f),ignore_index = True)
    #        #print(pd.read_json(f))
    #        df=pd.read_json(f)
    #        agent_data_tmp = df.props.pageProps['pageData']['agents']
    #        agent_data_merged = pd.append(agent_data_tmp)
    #        #dumb_merge= dumb_merge.append(pd.read_json(f),ignore_index = True)
        except:
            print('could not append file {}'.format(f))
            could_not_merge +=1
            pass

    return merged_json_data


def merge_csv(lst: list):
    #dumb_merge = pd.DataFrame()
    
   
    merged_csv_data = pd.DataFrame()
    could_not_merge = 0 
    for f in lst:
        try:

            merged_csv_data = merged_csv_data.append(pd.read_csv(f),ignore_index = True)
    #        #print(pd.read_json(f))
    #        df=pd.read_json(f)
    #        agent_data_tmp = df.props.pageProps['pageData']['agents']
    #        agent_data_merged = pd.append(agent_data_tmp)
    #        #dumb_merge= dumb_merge.append(pd.read_json(f),ignore_index = True)
        except:
            print('could not append file {}'.format(f))
            could_not_merge +=1
            pass
    #print (could_not_merge)
    return merged_csv_data

def load_json_files(dictionary: dict):
    os.chdir(dictionary['directories']['input_directory'])
    #f = dictionary['files']['files_to_merge'][2]
    #with open(f) as d:
    #    data = json.load(d)
    #    #print(data['results'][0])
    #df = pd.DataFrame(data['results'])
    #print(df)
    #print(len(data['results']))
    #print(f)
    json_df = pd.DataFrame()
    for f in dictionary['files']['files_to_merge']:
        with open(f) as d:
            data = json.load(d)
        df = pd.DataFrame(data["results"])
        
        json_df = pd.concat([json_df,df],ignore_index=True )

    
    
    #print(json_df['resources'][0][0]['pdf'])
    #print(json_df['item'][0])
    #print(type(json_df['item'][0]))

    os.chdir(dictionary['directories']['cwd'])

    return json_df

    #print(json_df)
    #counter = 0
    #for f in dictionary['files']['files_to_merge']:
    #    if counter == 0:
    #        with open(f) as d:
    #            data = json.load(d)
    #        json_df = pd.DataFrame(data["results"])
    #        counter +=1
    #    else:
    #        with open(f) as d:
    #            data = json.load(d)
    #            df = pd.DataFrame(data["results"])
        
    #        pd.concat([json_df,df])

    #print(json_df)



    
    #with open(dictionary['files']['files_to_merge'][0]) as f:
        #data = json.load(f)

    #print(data.keys())
    ##print(len(data["results"]))
    #df = pd.DataFrame(data["results"])
    #print(df.columns)

    #print(df)
    #print(data["content"])
    #print(data['content']['results'][0])
    #print(len(data['content']['results'])) 
    #print(len(data['results']))
    #print(len(data['content']))
    #print(json.dumps(data["content"], indent = 4, sort_keys=True))
    #jsonin = pd.DataFrame.from_dict(data,orient='index')
    #online = pd.read_json("https://www.loc.gov/collections/united-states-reports?fo=json&dates=2000/2099&fa=online-format:image%7Cpartof:u.s.+reports:+civil+procedure&sb=date")
    #print(online)
    #json = pd.concat([pd.read_json(f) for f in dictionary['files']['files_to_merge'] ],sort=True)
    #os.chdir(dictionary['directories']['cwd'])
    

