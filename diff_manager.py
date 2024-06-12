from deepdiff import DeepDiff
import json
import re
from dataclasses import dataclass
from path_manager import *

@dataclass
class DiffEntry(object):
    key: str
    diff: str

def convert_types_to_string(data):
    if isinstance(data, dict):
        return {key: convert_types_to_string(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_types_to_string(item) for item in data]
    elif isinstance(data, type):
        return str(data)
    else:
        return data

def getKey(id, obj):
    if isinstance(id, list):
        values = [str(obj.get(key, "0")) for key in id]
        # Join the values with '-' and enclose in brackets
        return "-".join(values)
    else:
        return obj[id];

def compare_records_by_id(dict1, dict2, id_key='id', ignore_items_removed = False, exclude_paths = [], **kwargs):
    dict1_by_id = {getKey(id_key, item): item for item in dict1}
    dict2_by_id = {getKey(id_key, item): item for item in dict2}
    # Find differences using DeepDiff for records with the same id

    differences = {}
    differencesArr = []
    for id_value in set(dict1_by_id.keys()).union(set(dict2_by_id.keys())):
        if id_value in dict1_by_id and id_value in dict2_by_id:
            diff = DeepDiff(dict1_by_id[id_value], dict2_by_id[id_value], ignore_order=True,exclude_paths=exclude_paths)
            if diff:
                #if(ignore_items_removed):
                    #del diff['dictionary_item_removed']

                differences[id_value] = diff
                differencesArr.append(DiffEntry(id_value,  convert_types_to_string(diff)))
        elif id_value in dict1_by_id:
            differences[id_value] = {'record_removed': dict1_by_id[id_value]}
            differencesArr.append(DiffEntry(id_value, {'record_removed': dict1_by_id[id_value]}))
        else:
            differences[id_value] = {'record_added': dict2_by_id[id_value]}
            differencesArr.append(DiffEntry(id_value, {'record_added': dict2_by_id[id_value]}))
    return differencesArr




def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def validate_and_write_ids(dict1, dict2, file_common, file_only_in_first, file_only_in_second, id_key='id'):
    # Find common IDs
    dict1_by_id = {getKey(id_key, item): item for item in dict1}
    dict2_by_id = {getKey(id_key, item): item for item in dict2}
    common_ids = set(dict1_by_id.keys()).intersection(set(dict2_by_id.keys()))

    # Find IDs only in the first dictionary
    only_in_first_ids = set(dict1_by_id.keys()).difference(set(dict2_by_id.keys()))

    # Find IDs only in the second dictionary
    only_in_second_ids = set(dict2_by_id.keys()).difference(set(dict1_by_id.keys()))


    print(f'\tCreated ... {file_common} Records ', len(common_ids))
    print(f'\tCreated ... {file_only_in_first} Records ', len(only_in_first_ids))
    print(f'\tCreated ... {file_only_in_second} Records ', len(only_in_second_ids))

    # Write common IDs to file
    with open(get_path(file_common), 'w') as f:
        for id in common_ids:
            f.write(f"{id}\n")

    # Write IDs only in the first dictionary to file
    with open(get_path(file_only_in_first), 'w') as f:
        for id in only_in_first_ids:
            f.write(f"{id}\n")

    # Write IDs only in the second dictionary to file
    with open(get_path(file_only_in_second), 'w') as f:
        for id in only_in_second_ids:
            f.write(f"{id}\n")

def checkDiff(filesListBase, filesListCompared, id, ignore_items_removed, ignore_path , **kwargs ):
    for fileRecordBase in filesListBase:
        fileToCompare =  next(x for x in filesListCompared if x.key ==fileRecordBase.key)
        print(f'Base {str(fileRecordBase)} ToCompare with {str(fileToCompare)}')


        json_data_base = load_json(get_path(fileRecordBase.path))
        json_data_compare_to= load_json(get_path(fileToCompare.path))
        validate_and_write_ids(json_data_base, json_data_compare_to, 'report-common_ids.txt', 'report-'+fileRecordBase.prefix + '_ids.txt', 'report-'+fileToCompare.prefix + '_ids.txt', id)

        differences = (compare_records_by_id
                       (json_data_base, json_data_compare_to,
                        id,
                        ignore_path,
                        ignore_items_removed,
                        **kwargs))
        if not differences:
            print(f"\tJSON objects are equal!!!!!!!!!!!! {fileRecordBase.key}")
        else:
            with open(get_path(f'diff-{fileRecordBase.key}.json'), 'w') as f:
                jsonF = json.dumps(differences, default=lambda o: o.__dict__)
                f.write(jsonF)
                print(f'\tCreated ... diff-{fileRecordBase.key}.json  Records ', len(differences))
        #pprint(jsonF)