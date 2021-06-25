import pandas as pd
import os
import json

cwd = os.getcwd()
sep = os.sep
input_dir = 'input'
input_dir = sep.join((cwd,input_dir))
#direct= sep.join((cwd,'data.json'))
file_extension ='.json'
output_direct = sep.join((cwd,"output.csv"))

def files_to_merge():
    os.chdir(input_dir)
    files_to_merge = [i for i in glob.glob('*.{}'.format(file_extension))]



def dumb_merge(files_to_merge):
    for f in files_to_merge:
        df=pd.read_json(f)
        agent_data_tmp = df.props.pageProps['pageData']['agents']
        agent_data_merged = pd.append(agent_data_tmp)
    return agent_data_merged

    #dumb_merge = pd.concat([pd.read_csv(f) for f in dictionary['files']['files_to_merge'] ],sort=True)
    
#print(agent_data[0])

agent_df.to_csv(output_direct)
#jsoner.to_csv(output_direct)

#print(data)
#print(len(jsoner.props.pageProps['pageData']['agents']))

#print(jsoner.props.pageProps['pageData']['agents'][0]['email'])
