#save this


num_rows = num_rows + len(normalized)
            for k,v in seen_columns.items():
                #try:
                d = normalized[v].tolist()
                print(d)
                rnge = "'Sheet1'" + "!" + k + str(start) + ":" + k + str(num_rows)
                print(rnge)
                print(v)
                for i in range(len(d)): 
                    if type(d[i]) is dict:
                        print("you have a dict")
                        string = ''
                        lst = d.values()
                        string = ','.join(lst)
                        index = string
                        pprint('joined the indexes in d..  Hopefull it looks like {}'.format(d))
                    elif type(d[i]) is list:
                        print("you have a list")
                        print(d[i])
                        for j in range(len(d[i])):
                            if type(d[i][j]) is dict:
                                normal = pd.json_normalize(d[i][j])
                                print(normal)
                                print('     you have a dict in the lst')
                                lst = d[i][j].values()
                                string = ','.join(lst)
                                d[i][j] = string
                        d[i] = ','.join(d[i])
                        print(d[i])

                                
                    else:
                        print('you have a {}'.format(type(index)))
                
    
                print(d)
                body = {
                    "majorDimension": "COLUMNS",
                    "values": [d]
                }
                #rnge = rnge    
                #valueInputOption="USER_ENTERED"
                print(v)
                request = sheets_service.values().append(spreadsheetId=spreadsheet_id, range=rnge, valueInputOption="RAW", body=body)
                respie = request.execute()
                
                pprint(respie)
                #except:
                 #   print("the key {} is not in this df or append fail".format(v))
           
            pprint(seen_columns)
            print(num_rows)
            
            
            

            



            #pprint(normalized['nrds_id'])

            #for agent in data['props']['pageProps']['pageData']['agents']:
            #    df_f.clean_agent_data(agent)
                #print(type(agent))
                #print(type(data['props']['pageProps']['pageData']['agents']))
                #pprint(agent)

                

                
                #data['state'] = state
                #data['city'] = city
                
                #df_f.clean_realtor_data(data.props.pageProps['pageData'])
                #df_f.filter_realtor_data(dictionary['tasks']['environmental_vars']['dfs']['merged_agent_data'],df,800000,3)
                
              
           # except:
           #     print("no more to people to parse.. :(")
                
                

            start = num_rows
            time.sleep(random.randint(45,60))

        print('You scraped {} pages'.format(n_pages))


                

    