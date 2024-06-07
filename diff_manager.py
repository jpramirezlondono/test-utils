from deepdiff import DeepDiff
import json
import re
from dataclasses import dataclass
import pprint

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

def compare_records_by_id(dict1, dict2, id_key='id'):
    dict1_by_id = {item[id_key]: item for item in dict1}
    dict2_by_id = {item[id_key]: item for item in dict2}
    # Find differences using DeepDiff for records with the same id
    differences = {}
    differencesArr = []
    for id_value in set(dict1_by_id.keys()).union(set(dict2_by_id.keys())):
        if id_value in dict1_by_id and id_value in dict2_by_id:
            diff = DeepDiff(dict1_by_id[id_value], dict2_by_id[id_value], ignore_order=True)
            if diff:
                differences[id_value] = diff
                differencesArr.append(DiffEntry(id_value,  convert_types_to_string(diff)))
        elif id_value in dict1_by_id:
            differences[id_value] = {'record_removed': dict1_by_id[id_value]}
            differencesArr.append(DiffEntry(id_value, {'record_removed': dict1_by_id[id_value]}))
        else:
            differences[id_value] = {'record_added': dict2_by_id[id_value]}
            differencesArr.append(DiffEntry(id_value, {'record_removed': dict2_by_id[id_value]}))
    return differencesArr




def load_json(file_path):
    basepath = ''
    with open(basepath +file_path, 'r') as file:
        return json.load(file)

def checkDiff(filesListBase, filesListCompared, ID):
    for fileRecordBase in filesListBase:
        fileRecord =  next(x for x in filesListCompared if x.key ==fileRecordBase.key)
        print(f'Base {str(fileRecordBase)} ToCompare with {str(fileRecord)}')

        with open(f'diff-{fileRecordBase.key}.json', 'w') as f:
            json_data1 = load_json(fileRecordBase.path)
            json_data2 = load_json(fileRecord.path)
            differences = compare_records_by_id(json_data1, json_data2, ID)
            if not differences:
                print(f"JSON objects are equal {fileRecordBase.key}")
            else:
                #print("JSON objects are different")
                #jsonF = json.dumps(differences, indent=4)
                jsonF = json.dumps(differences, default=lambda o: o.__dict__)
                #print(jsonF)
                f.write(jsonF)
            #pprint(jsonF)