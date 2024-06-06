import json
import logging
from io import open
from deepdiff import DeepDiff

# Function to load JSON data from a file
def load_json(file_path):
    basepath = '/Users/jramirezlondono/Documents/'
    with open(basepath +file_path, 'r') as file:
        return json.load(file)

def calculate_diff (path1, path2):
    json_data1 = load_json(path1)
    json_data2 = load_json(path2)
    # Compare the JSON objects using DeepDiff
    differences = DeepDiff(json_data1, json_data2, ignore_order=True, log_frequency_in_sec=40, progress_logger=logging.warning, max_diffs = 852993).to_dict()

    # Output the differences
    if not differences:
        print("JSON objects are equal")
    else:
        print("JSON objects are different")
        jsonF = json.dumps(differences, indent=4)
        print(jsonF)


#Diferent values a vs b
def load_test1():
    # Paths to the JSON files
    #file1_path = 'response-nemo.json'
    #file2_path = 'response-rpc.json'
    file1_path = 'GetAllSeparatedByTeamNemo.json'
    file2_path = 'GetAllSeparatedByTeamGrpc.json'
    # Load JSON data from the files
    calculate_diff(file1_path, file2_path)

#Same values
def load_test2():
    # Paths to the JSON files
    #file1_path = 'response-nemo.json'
    #file2_path = 'response-rpc.json'
    file1_path = 'GetAllSeparatedByTeamNemo.json'
    file2_path = 'GetAllSeparatedByTeamNemo.json'
    # Load JSON data from the files
    calculate_diff(file1_path, file2_path)

#Diferent values b vs a
def load_test3():
    # Paths to the JSON files
    #file1_path = 'response-nemo.json'
    #file2_path = 'response-rpc.json'
    file2_path = 'GetAllSeparatedByTeamNemo.json'
    file1_path = 'GetAllSeparatedByTeamGrpc.json'
    # Load JSON data from the files
    calculate_diff(file1_path, file2_path)

#load_test1()
#load_test2()
#load_test3()