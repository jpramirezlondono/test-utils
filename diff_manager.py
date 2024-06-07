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

def compare_records_by_id(dict1, dict2, id_key='id', ignore_type_in_groups = False, ignore_items_removed = False, exclude_paths = [], **kwargs):
    dict1_by_id = {item[id_key]: item for item in dict1}
    dict2_by_id = {item[id_key]: item for item in dict2}
    # Find differences using DeepDiff for records with the same id
    differences = {}
    differencesArr = []
    for id_value in set(dict1_by_id.keys()).union(set(dict2_by_id.keys())):
        if id_value in dict1_by_id and id_value in dict2_by_id:
            diff = DeepDiff(dict1_by_id[id_value], dict2_by_id[id_value], ignore_order=True,exclude_paths=exclude_paths, ignore_type_subclasses=True )
            if diff:
                if(ignore_items_removed):
                    del diff['dictionary_item_removed']
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

def checkDiff(filesListBase, filesListCompared, id, ignore_type_in_groups, ignore_items_removed, ignore_path , **kwargs ):
    for fileRecordBase in filesListBase:
        fileRecord =  next(x for x in filesListCompared if x.key ==fileRecordBase.key)
        print(f'Base {str(fileRecordBase)} ToCompare with {str(fileRecord)}')

        json_data_base = load_json(get_path(fileRecordBase.path))
        json_data_compare_to= load_json(get_path(fileRecord.path))
        differences = compare_records_by_id(json_data_base, json_data_compare_to, id, ignore_type_in_groups, ignore_items_removed, ignore_path, **kwargs)
        if not differences:
            print(f"\tJSON objects are equal!!!!!!!!!!!! {fileRecordBase.key}")
        else:
            with open(get_path(f'diff-{fileRecordBase.key}.json'), 'w') as f:
                jsonF = json.dumps(differences, default=lambda o: o.__dict__)
                f.write(jsonF)
                print(f'\tCreated ... diff-{fileRecordBase.key}.json  Records ', len(differences))
        #pprint(jsonF)