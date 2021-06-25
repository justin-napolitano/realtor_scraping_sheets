#filter.py
from pprint import pprint

def clean_agent_data(agent_dict):
    #print(df)
    #df['count'] = ''
    #df['min_price'] = ''
    #df['max_price'] = ''
    #df['aproximate_listing_value'] = ''
    #print(df.columns)
    #print(df['for_sale_price'][0]['max'])
    href = agent['href']
    first_name = agent['first_name']
    last_name = agent['last_name']
    mls = agent['mls']
    nick_name = agent['nick_name']
    #name = 
    pprint(agent_dict)
    for k,v in agent_dict.items():
        print(k)

def obsolete():
    for i in range(0,len(df)):
        #lst = lst.append
        #print(df.at[i, 'for_sale_price']['count'])
        
        #set max
        min_price = df.at[i, 'for_sale_price']['min'] 

        max_price = df.at[i, 'for_sale_price']['max']
        #set count
        count = df.at[i, 'for_sale_price']['count']
        #set count in df
        df.at[i, 'listings'] = count
        #set listing value according to estimatoin
        df.at[i, 'aproximate_listing_value'] = ((min_price + max_price)/2) * count



    df.drop(df.columns.difference(['full_name','first_name', 'last_name','email','listings','aproximate_listing_value',]), 1, inplace=True)
    df["full_name"] = df["full_name"].str.lower()
    df["first_name"] = df["first_name"].str.lower()
    df["last_name"] = df["last_name"].str.lower()

    #print(df)




    
    #df['aproximate_listing_value'] = df['for_sale']['count']* ((df['for_sale']['min'] + df['for_sale']['max'])/2) 
    

def filter_realtor_data(df, dnn ,min_val: int,min_listings: int):


    filter1 = df["listings"] > min_listings

    # making boolean series for age
    filter2 = df["aproximate_listing_value"]>= min_val
    filter3 = df.first_name.isin(df2.first_name)
    filter4 = df.last_name.isin(df2.last_name)
    #print(df2)
    #df.where(filter3 & filter4, inplace = True)

    df.where(filter1, inplace = True)
    df.mask(filter3 & filter4, inplace = True)
    df.dropna(inplace = True)
    df.drop_duplicates(inplace = True)
    #print(df)

    #print(df)




def filter_state_data(df, state:str):


    filter1 = df["state"] == state
    filter2 = df['searched']  == 0
    # making boolean series for age


    df.where(filter1 & filter2, inplace = True)
    df.dropna(inplace = True)
    #df.drop_duplicates(inplace = True)
    #print(df)

    #print(df)



