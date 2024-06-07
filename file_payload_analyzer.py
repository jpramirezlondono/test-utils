
import sys
import os
import json
import math
import pandas as pd
from dataclasses import dataclass
from diff_manager import *

MAX_RECORDS = 10

@dataclass
class File(object):
    key: str
    path: str

def loadFile_and_split_by_root_entry(prefix, file_name, sortKey):
    thislist = []
    try:
        # request file name
        f = open(file_name)
        file_size = os.path.getsize(file_name)
        data = json.load(f)
        root_keys = list(data.keys())
        #print(root_keys)

        keys_to_split = root_keys
        # Split the object into smaller objects based on the keys
        split_data = {key: data[key] for key in keys_to_split}
        # Save each smaller object into a separate file
        for key, value in split_data.items():
            with open(f'{prefix}-{key}.json', 'w') as f:
                df2 = pd.DataFrame(value)
                df2[[sortKey]] = df2[[sortKey]].astype(int)
                sorted = df2.sort_values(by=[sortKey])
                sorted_data_list = sorted.to_dict(orient="records")
                if( MAX_RECORDS != 0 ):
                    sorted_data_list = sorted_data_list[:MAX_RECORDS]
                sorted_data_list_pretty = json.dumps(sorted_data_list, indent=4)
                if( MAX_RECORDS != 0 ):
                    records = len(sorted_data_list)
                else:
                    records = len(df2.index)
                f.write(sorted_data_list_pretty)
                tfile_size = os.path.getsize(f'{prefix}-{key}.json')
                print(f'Created ... {prefix}-{key} Records {records} with size {tfile_size}')
                fileRecord = File(key, f'{prefix}-{key}.json')
                thislist.append(fileRecord)
                #print(sorted_data_list_pretty)
    except:
        print(exception)
        print('Error loading JSON file ... exiting')
    return thislist



ID = "pmCampaignId"

fileListNemo = loadFile_and_split_by_root_entry("nemo", "/Users/jramirezlondono/Documents/response-nemo-1.json", ID)
fileListGRPC = loadFile_and_split_by_root_entry("grpc", "/Users/jramirezlondono/Documents/response-rpc-1.json", ID)
#print(str(fileListNemo))
#print(str(fileListGRPC))
checkDiff(fileListNemo, fileListGRPC, ID)
