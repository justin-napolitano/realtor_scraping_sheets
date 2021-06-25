#clean_df.py

import pandas as pd
import glob
import os
import log as log
import gc


def clean_df(json_dirty_df):
    drop_columns = ['id','date','dates', 'hassegments','access_restricted','aka','campaigns','contributor','digitized','group','extract_timestamp','language','image_url','index','mime_type','online_format','original_format','other_title','partof','subject','timestamp','type']
    json_dirty_df.drop(columns = drop_columns,inplace = True)
    #print(json_dirty_df.columns)


def series_col(df):
    #file_location_df['shelf_id'] = df["shelf_id"] 
    #file_location = df['shelf_id'] + df['title'] + df["item"][call_number]
    #df['file_location'] = file_location
    df['series'] = None
    unique_series_list = []
    df_len = len(df)
    i = 0
    #print(df['item'][300]["call_number"])
    while i < df_len:
        series_list = []
        for item in df['item'][i]["call_number"]:
            tup = tuple(item.split(": "))
            if tup[0] != "Call Number":
                tmp = tup[1]
                tmp = tmp.replace(" ","-")
                series_list.append(tmp)
                if tmp not in unique_series_list:
                    unique_series_list.append(tmp)
                else:
                    continue
            else: 
                continue
        
        
        #series =  ','.join(map(str, series_list))
        df['series'][i]= series_list
        #unique_series_list
        i +=1
        
    #print(df['series'])

def subject_col(df):
    #file_location_df['shelf_id'] = df["shelf_id"] 
    #file_location = df['shelf_id'] + df['title'] + df["item"][call_number]
    #df['file_location'] = file_location
    df['subject'] = None
    unique_subject_list = []
    df_len = len(df)
    i = 0
    while i < df_len:
        subject_list = []
        for item in df['item'][i]["subjects"]:
            tmp = item.replace(" ","-")
            subject_list.append(tmp)
            if item not in unique_subject_list:
                unique_subject_list.append(tmp)
            else: 
                continue
        
    
        #print(subjects)
        df['subject'][i] = subject_list
        i +=1
    #print(unique_subject_list)

def pdf_col(df):
    #file_location_df['shelf_id'] = df["shelf_id"] 
    #file_location = df['shelf_id'] + df['title'] + df["item"][call_number]
    #df['file_location'] = file_location
    df['pdf'] = None
    df_len = len(df)
    i = 0
    while i < df_len:
        item = df['resources'][i][0]["pdf"]
        df['pdf'][i] = item
        i += 1
        
    #print(df['series'][0])
    #print(df["subject"][0])
    #print(df.columns)
    #print(df['resources'])
   
def output_df(df,dictionary):
    output_df = pd.DataFrame({"shelf_id": [], "title": [], "series": [], "subject": [], "pdf": [], "url": []})
    sep = os.sep
    tmp_dict = {"shelf_id": None, "title": None, "series": None, "subject": None, "pdf": None, "url": None}
    unique_series_list = []
    unique_subject_list = []
    #print(dictionary)
    for index, row in df.iterrows():
        for serie in row['series']:
            for subject in row['subject']:
                tmp_dict['shelf_id'] = row['shelf_id']
                tmp_dict['title'] = row['title']
                tmp_dict['series'] = serie
                tmp_dict['subject'] = subject
                tmp_dict['pdf'] = row['pdf']
                tmp_dict['url'] = row['url']
                if serie not in unique_series_list:
                    serie=serie.lower()
                    unique_series_list.append(serie)
                if subject not in unique_subject_list:
                    subject= subject.lower()
                    unique_subject_list.append(subject)
                #tmp_df = pd.DataFrame(tmp_dict)
                #print(tmp_dict)

                output_df = output_df.append(tmp_dict,ignore_index=True)
    #print(unique_series_list)
    #print(unique_subject_list)
    dictionary["unique_series_list"] = unique_series_list
    dictionary['unique_subject_list'] = unique_subject_list
    return output_df
    #print(garbage_log.objects)

  




    #print(output_df['series'])

         
                    
                

    
    #while i < df_len:
    #    item = df['resources'][i][0]["pdf"]
    #    df['pdf'][i] = item
    #    i += 1

   