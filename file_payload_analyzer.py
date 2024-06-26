
import sys
from sys import getsizeof
import os
import json
import math
import time
import pandas as pd
from dataclasses import dataclass
from diff_manager import *
from path_manager import *

MAX_RECORDS = 100

@dataclass
class File(object):
    key: str
    path: str
    prefix: str

def loadFile_and_split_by_root_entry(prefix, file_name, sortKey):
    #delete_tmp_folder()
    thislist = []
    try:
        # request file name
        file_in_text = open(file_name)
        data = json.load(file_in_text)
        root_keys = list(data.keys())

        keys_to_split = root_keys
        # Split the object into smaller objects based on the keys
        split_data = {key: data[key] for key in keys_to_split}
        # Save each smaller object into a separate file
        for key, value in split_data.items():
            with open(get_path(f'{prefix}-{key}.json'), 'w') as f:
                panadas_dataFrame = pd.DataFrame(value)
                if isinstance(sortKey, list):
                    for k in sortKey:
                        panadas_dataFrame[k] = panadas_dataFrame[k].astype(int)
                    sorted_data = panadas_dataFrame.sort_values(by=sortKey)
                else:
                    panadas_dataFrame[[sortKey]] = panadas_dataFrame[[sortKey]].astype(int)
                    sorted_data = panadas_dataFrame.sort_values(by=[sortKey])
                sorted_data_list = sorted_data.to_dict(orient="records")
                total_size = getsizeof(sorted_data)
                total_records = len(sorted_data_list)
                if( MAX_RECORDS != 0 ):
                    sorted_data_list = sorted_data_list[:MAX_RECORDS]
                sorted_data_list_pretty = json.dumps(sorted_data_list, indent=4)
                if( MAX_RECORDS != 0 ):
                    records = len(sorted_data_list)
                else:
                    records = len(panadas_dataFrame.index)
                f.write(sorted_data_list_pretty)
                tfile_size = os.path.getsize(get_path(f'{prefix}-{key}.json'))
                if( MAX_RECORDS != 0 ):
                    print(f'Created ... {prefix}-{key} Records {records} with size {tfile_size} out of {total_records} Records total size {total_size}')
                else:
                    print(f'Created ... {prefix}-{key} Records {records} with size {tfile_size}')

                fileRecordInstance = File(key, f'{prefix}-{key}.json', prefix )
                thislist.append(fileRecordInstance)

    except:
        print(exception)
        print('Error loading JSON file ... exiting')
    return thislist

# Capture the start time
start_time = time.time()
print("Application starting ...")

#Key to sort and to identify the records
ID = ["pmCampaignId","measurementSourceId"]
IGNORE_DICTIONARY_ITEMS_REMOVED = False
IGNORE_PATH = ["root['iasCampaignName']","root['createdOn']","root['salesforceTicketUrl']"]
IGNORE_TYPES = ["root['reason']", "root['pmVendorClientId']", "root['iasCampaignName']", "root['createdOn']"]


fileListBase = (loadFile_and_split_by_root_entry
                ("nemo", "/Users/jramirezlondono/Documents/response-nemo.json", ID
                ))
fileListToCompare = (loadFile_and_split_by_root_entry
                ("grpc",
                 "/Users/jramirezlondono/Documents/response-grpc.json", ID
                 ))
#print(str(fileListNemo))
#print(str(fileListGRPC))
checkDiff(fileListBase, fileListToCompare, ID,
          IGNORE_DICTIONARY_ITEMS_REMOVED, IGNORE_PATH,
          IGNORE_TYPES
          )


end_time = time.time()
# Calculate the duration
duration = end_time - start_time
# Print the duration
print(f"Application ran for {duration:.2f} seconds")
