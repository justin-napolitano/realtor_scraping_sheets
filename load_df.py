#load_df.py
import pandas as pd
import glob
import os
import log as log
import json

def load_cases_df(dictionary: dict):
    #print(dictionary['download_pdf']['directories'])
    os.chdir(dictionary['download_pdf']['directories']['read_directory'])
    working_file = glob.glob('*.{}'.format(dictionary['load_json_files']['files']['output_extension']))
    #print(working_file)
    json_df = pd.DataFrame()
    for f in working_file:
        with open(f) as d:
            data = json.load(d)
        df = pd.DataFrame(data)
            
        json_df = pd.concat([json_df,df],ignore_index=True )
    #print(json_df)
    #print(json_df.columns)
    return json_df



def load_POC(dictionary: dict):
    os.chdir(dictionary['dumb_merge']['directories']['output_directory'])
    working_file = glob.glob('*.{}'.format(dictionary['create_POC_table']['files']['output_extension']))
    master_df = pd.concat([pd.read_csv(f) for f in working_file],sort=True)
    points_of_contact = master_df[master_df["POC"] == 1]
    print(points_of_contact.columns)
    #poc = points_of_contact['POC']
    os.chdir(dictionary['dumb_merge']['directories']['cwd'])
    return points_of_contact

def load_company_table(dictionary: dict):
    os.chdir(dictionary['dumb_merge']['directories']['output_directory'])
    working_file = glob.glob('*.{}'.format(dictionary['create_company_table']['files']['output_extension']))
    df = pd.concat([pd.read_csv(f) for f in working_file],sort=True)
    #print(df)
    company_table = df.groupby(['Company name']).head(1)
    #print(company_table)
    os.chdir(dictionary['dumb_merge']['directories']['cwd'])
    return company_table
    #print(Truth.groupby(by="Company name").indices)
    #print(NotTrue.groups)
    #print(NotTrue)

def unsubcribe_master(dictionary: dict):
    os.chdir(dictionary['dumb_merge']['directories']['output_directory'])
    master_file = glob.glob('*.{}'.format(dictionary['unsubscribe']['files']['output_extension']))
    master_df = pd.concat([pd.read_csv(f) for f in master_file],sort=True)

    os.chdir(dictionary['unsubscribe']['directories']['input_directory'])
    subscriber_file = glob.glob('*.{}'.format(dictionary['unsubscribe']['files']['output_extension']))
    unsubscribers_df = pd.concat([pd.read_csv(f) for f in subscriber_file],sort=True)

    unsubscribe_email_list = unsubscribers_df['Email address'].tolist()
    print(unsubscribe_email_list)

    #filter = master_df['Email address'] == unsubscribe_email_list

    for email in unsubscribe_email_list:
        email = email.lower()
        master_df.loc[master_df["Email address"] == email, 'subscriber'] = 0
    
    os.chdir(dictionary['dumb_merge']['directories']['cwd'])

    return master_df, unsubscribers_df

def unsubscribe_batches(dictionary: dict):

    os.chdir(dictionary['unsubscribe']['directories']['input_directory'])
    subscriber_file = glob.glob('*.{}'.format(dictionary['unsubscribe']['files']['output_extension']))
    unsubscribers_df = pd.concat([pd.read_csv(f) for f in subscriber_file],sort=True)

    os.chdir(dictionary['batch_merge']['directories']['output_directory'])
    master_file = glob.glob('*.{}'.format(dictionary['unsubscribe']['files']['output_extension']))
    master_df = pd.concat([pd.read_csv(f) for f in master_file],sort=True)

    unsubscribe_email_list = unsubscribers_df['Email address'].tolist()
    #print(unsubscribe_email_list)


    for i in master_file:
        csv_file = i
        print(i)
        df = pd.read_csv(csv_file)

        for email in unsubscribe_email_list:
            email = email.lower()
            df.loc[df["Email address"] == email, 'subscriber'] = 0

        yield df


    #unsubscribers = df.groupby(['Company name']).head(1)
    #os.chdir(dictionary['dumb_merge']['directories']['cwd'])