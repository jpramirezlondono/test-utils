from deepdiff import DeepDiff
import json


def compare_records_by_id(dict1, dict2, id_key='id'):
    dict1_by_id = {item[id_key]: item for item in dict1}
    dict2_by_id = {item[id_key]: item for item in dict2}
    # Find differences using DeepDiff for records with the same id
    differences = {}
    for id_value in set(dict1_by_id.keys()).union(set(dict2_by_id.keys())):
        if id_value in dict1_by_id and id_value in dict2_by_id:
            diff = DeepDiff(dict1_by_id[id_value], dict2_by_id[id_value], ignore_order=True)
            if diff:
                differences[id_value] = diff
        elif id_value in dict1_by_id:
            differences[id_value] = {'record_removed': dict1_by_id[id_value]}
        else:
            differences[id_value] = {'record_added': dict2_by_id[id_value]}
    return differences




def load_json(file_path):
    basepath = ''
    with open(basepath +file_path, 'r') as file:
        return json.load(file)

def checkDiff(filesListBase, filesListCompared, ID):
    for fileRecordBase in filesListBase:
        print(f'Base{str(fileRecordBase)}')
        fileRecord =  next(x for x in filesListCompared if x.key ==fileRecordBase.key)
        print(f'ToCompare{str(fileRecord)}')

        json_data1 = load_json(fileRecordBase.path)
        json_data2 = load_json(fileRecord.path)
        differences = compare_records_by_id(json_data1, json_data2, ID)
        if not differences:
            print("JSON objects are equal")
        else:
            print("JSON objects are different")
            #jsonF = json.dumps(differences, indent=4)
            print(differences)