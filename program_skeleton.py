#program_skeleton.py
#import load_json_files as bm

import write
import merge as m
import load_df as ldf
import load_vars as lv
import log as log
import clean_df as clean
import download as dl
import gc
import confirm_drcts as cfs
import fix_files as ff
import readwrite as rw
import df_filter as df_f
import realtor_scraper_sheets_4 as scraper
import get_creds as creds
import goog_sheets as sheets
from pprint import pprint
import google_drive as drive
import batch_download as download
import rew_scraper as rew_scraper
import rew_scraper3 as rew3


def program_skeleton(dictionary: dict):

## Batch Merge creates a back_up of contacts from csv in batches no greater than 500 contacts per document.  Can be expanded.  Keeps files from getting to large
 
    
    if dictionary['tasks']['environmental_vars']['run'] == True:
        dictionary['tasks']['environmental_vars']['log']['environmental_vars_set'] = lv.set_environmental_vars(dictionary['tasks'])
        dictionary['tasks']['environmental_vars']['goog_creds'] = creds.get_creds()
        dictionary['tasks']['environmental_vars']['sheets_service'] = sheets.get_sheet_service(dictionary['tasks']['environmental_vars']['goog_creds'])
        dictionary['tasks']['environmental_vars']['drive_service'] = drive.get_drive_service(dictionary['tasks']['environmental_vars']['goog_creds'])
        dictionary['tasks']['environmental_vars']['criteria_sheet_meta'] = sheets.confirm_sheet_ids(dictionary['tasks']['environmental_vars']['criteria_sheet_ids'],dictionary['tasks']['environmental_vars']['sheets_service'])
        #dictionary['tasks']['environmental_vars']['output_sheet_meta'] =  drive.add_spreadsheet_to_folder(dictionary['tasks']['environmental_vars']['drive_service'],dictionary['tasks']['environmental_vars']['output_folder_id'],dictionary['tasks']['environmental_vars']['date']['datetime'])
       
        #dictionary['tasks']['environmental_vars']['dfs']['cities_search'] = goog_sheets.
        #pprint(dictionary['tasks']['environmental_vars']['sheet_meta'])
        lv.batchify(dictionary['tasks']['environmental_vars']['criteria_sheet_meta'],dictionary['tasks']['environmental_vars']['batch_size'])
        dictionary['tasks']['environmental_vars']['dnn'] = sheets.batch_download(dictionary['tasks']['environmental_vars']['criteria_sheet_meta']['dnn'],dictionary['tasks']['environmental_vars']['sheets_service'],True)
        
        #sheets.batch_download(dictionary['tasks']['environmental_vars'])
        #print(dictionary['tasks']['environmental_vars']['directories']['log_directory'])
        #log.json_dump(dictionary['tasks'])
        #log.csv_dump(dictionary['tasks'])
        #print(dictionary)
    if dictionary['tasks']['scrape_web_data_rew']['run'] == True:
        #if dictionary['tasks']['scrape_web_data_sheets']['input_list']['run'] == True:
        #pprint(dictionary['tasks']['environmental_vars']['criteria_sheet_meta'])
        #input_df = sheets.batch_download(dictionary['tasks']['environmental_vars']['criteria_sheet_meta']['input_list'],dictionary['tasks']['environmental_vars']['sheets_service'],True)
        dictionary['tasks']['environmental_vars']['input_list'] = sheets.batch_download(dictionary['tasks']['environmental_vars']['criteria_sheet_meta']['input_list'],dictionary['tasks']['environmental_vars']['sheets_service'],True)
        #pprint(dictionary['tasks']['environmental_vars']['sheets_service'])
        rew3.initial(dictionary['tasks']['environmental_vars']['input_list'],dictionary['tasks']['environmental_vars']['sheets_service'])
        #rew_scraper.scrape("agents/areas/toronto-on",dictionary['tasks']['environmental_vars']['sheets_service'],2,2)
        #print('true')

    if dictionary['tasks']['scrape_web_data_sheets']['run'] == True:
        if dictionary['tasks']['scrape_web_data_sheets']['input_list']['run'] == True:
            #pprint(dictionary['tasks']['environmental_vars']['criteria_sheet_meta'])
            #input_df = sheets.batch_download(dictionary['tasks']['environmental_vars']['criteria_sheet_meta']['input_list'],dictionary['tasks']['environmental_vars']['sheets_service'],True)
            dictionary['tasks']['environmental_vars']['input_list'] = sheets.batch_download(dictionary['tasks']['environmental_vars']['criteria_sheet_meta']['input_list'],dictionary['tasks']['environmental_vars']['sheets_service'],True)
            scraper.scrape(dictionary['tasks']['environmental_vars']['input_list'],dictionary['tasks']['environmental_vars']['sheets_service'],dictionary['tasks']['environmental_vars']['drive_service'],dictionary['tasks']['environmental_vars']['output_folder_id'])
            #print('true')
            


            #download.batch_download(dictionary['tasks']['environmental_vars'])
         



    if dictionary['tasks']['confirm_folder_structure']['run'] == True:
        dictionary['tasks']['confirm_folder_structure']['log']['folder_structure_confirmed'] = cfs.confirm_folder_structure(dictionary)
        #ff.fix_files(dictionary) # fix files if necessary.  This is a fuck up on my end...
    
    if dictionary['tasks']['scrape_web_data']['run'] == True:
        dictionary['tasks']['scrape_web_data']['log']['cities'] = rw.file_list(dictionary['tasks']['environmental_vars']['directories']['cities'])
        df = dictionary['tasks']['environmental_vars']['dfs']['cities'] = m.merge_zip_data(dictionary['tasks']['scrape_web_data']['log']['cities'])
        df_f.filter_state_data(df,'ct')
        #dictionary['tasks']['environmental_vars']['dfs']['cities']['directory'] = df. apply dictionary['tasks']['environmental_vars']['sep'].join((dictionary['tasks']['environmental_vars']['directories']['to_merge'],  dictionary['tasks']['environmental_vars']['dfs']['cities'].state_name,dictionary['tasks']['environmental_vars']['dfs']['cities'].city))
        df['to_merge'] = dictionary['tasks']['environmental_vars']['directories']['to_merge']
        df['directory'] = df[['to_merge','state_name', 'city']].apply(lambda x: dictionary['tasks']['environmental_vars']['sep'].join(x), axis=1)
        #df['period'] = df[['Year', 'quarter']].apply(lambda x: ''.join(x), axis=1)
        #print(dictionary['tasks']['environmental_vars']['dfs']['cities'].directory)
        scraper.scrape(df)


        #dictionary['tasks']['environmental_vars']['dfs'][''] = m.merge_zip_data(dictionary['tasks']['scrape_web_data']['log']['zip_codes'])
        #dictionary['tasks']['environmental_vars']['dfs']['zip_codes'] = rw.file_list(dictionary['tasks']['environmental_vars']['files']['zip_database'])

    if dictionary['tasks']['merge_data']['run'] == True:
        dictionary['tasks']['merge_data']['log']['files_to_merge'] = rw.file_list_walk(dictionary['tasks']['environmental_vars']['directories']['to_merge'])
        dictionary['tasks']['environmental_vars']['dfs']['master_merge'] = m.merge_agent_data(dictionary['tasks']['merge_data']['log']['files_to_merge'])
        #rw.df_toJson(dictionary['tasks'],dictionary['tasks']['environmental_vars']['file_names']['master_merge'],dictionary['tasks']['environmental_vars']['dfs']['master_merge'],dictionary['tasks']['environmental_vars']['directories']['merged_data'])
        rw.df_toCsv(dictionary['tasks'],dictionary['tasks']['environmental_vars']['file_names']['agent_data_raw'],dictionary['tasks']['environmental_vars']['dfs']['master_merge'],dictionary['tasks']['environmental_vars']['directories']['merged_data'])
        rw.df_toJson(dictionary['tasks'],dictionary['tasks']['environmental_vars']['file_names']['agent_data_raw'],dictionary['tasks']['environmental_vars']['dfs']['master_merge'],dictionary['tasks']['environmental_vars']['directories']['merged_data'])
        #print(dictionary['tasks']['environmental_vars']['dfs']['master_merge'])

    if dictionary['tasks']['filter_data']['run'] == True:
        print('filtering_data')
        dictionary['tasks']['filter_data']['log']['files_to_filter'] = rw.file_list(dictionary['tasks']['environmental_vars']['directories']['merged_data'])
        dictionary['tasks']['filter_data']['log']['dnn_filter'] = rw.file_list(dictionary['tasks']['environmental_vars']['directories']['dnn'])
        
        
        df = dictionary['tasks']['environmental_vars']['dfs']['dnn'] = m.merge_csv(dictionary['tasks']['filter_data']['log']['dnn_filter'])
       
        df["first_name"] = df["first_name"].str.lower()
        df["last_name"] = df["last_name"].str.lower()
        ## checks to see if the df is already in memory.  If not the pass 
        try:
            if dictionary['tasks']['environmental_vars']['dfs']['merged_agent_data'].empty:
                #if try succeeds and if is true then fill it anyways
                dictionary['tasks']['environmental_vars']['dfs']['merged_agent_data'] = m.merge_json(dictionary['tasks']['filter_data']['log']['files_to_filter'])
        
            else:
                #if alrady exists move on
                print('The Df already exists')
                pass
                #do something
        except:
            #if exception is raised then the df does not exist.  Create it
             print('The Df no exists')
             dictionary['tasks']['environmental_vars']['dfs']['merged_agent_data'] = m.merge_json(dictionary['tasks']['filter_data']['log']['files_to_filter'])

            
      
        df_f.clean_realtor_data(dictionary['tasks']['environmental_vars']['dfs']['merged_agent_data'])
        df_f.filter_realtor_data(dictionary['tasks']['environmental_vars']['dfs']['merged_agent_data'],df,800000,3)

        rw.df_toCsv(dictionary['tasks'],dictionary['tasks']['environmental_vars']['file_names']['agent_data_mapped'],dictionary['tasks']['environmental_vars']['dfs']['merged_agent_data'],dictionary['tasks']['environmental_vars']['directories']['mapped_data'])
        rw.df_toJson(dictionary['tasks'],dictionary['tasks']['environmental_vars']['file_names']['agent_data_mapped'],dictionary['tasks']['environmental_vars']['dfs']['merged_agent_data'],dictionary['tasks']['environmental_vars']['directories']['mapped_data'])


       
        
        






    #if dictionary['tasks']['extract_agent_data']['run'] == True:
    #    dictionary['tasks']['environmental_vars']['dfs']['agent_data'] = m.merge_agent_data(dictionary['tasks'])


        

        

    