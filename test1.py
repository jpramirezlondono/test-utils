'''
def call_admantx(api_key, name, idProfile):
 # response = requests.get("http://loft10299.dedicatedpanel.com/apiservices/staging/getSegmentsByProfile?apikey="+api_key)
 segments = []
 # if response.text:
 #   json_object = json.loads(response.text)
 #   for segment in json_object["data"]:
 #           segments.append(segment["segment.ias_code"])
 profile = createProfile(segments,name,idProfile)
 return profile


array 1 vs. array 2

check size
sort by id
extract set(id from array 1) vs set(id from array 2), use Set function to compare to find out if two sets are the same
If sets are different, print out the diff
ids only in set 1
ids only in set 2
ids are common in both set1 and set 2
For ids common in set 1 and 2
loop through each object and compare the two objects with the same id
print out equal or not for the id
'''
import json
from CheckSize import CheckSize

# STEP 2: sort by id:
class Sort(object):
    def __init__(self):
        self.file_name_v1 = 'oldEp.json';
        self.file_name_v2 = 'newEp.json';

if __name__ == '__main__':

    CheckSize().execute()