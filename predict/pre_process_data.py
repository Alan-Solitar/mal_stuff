import pandas as pd
from pandas.io.json import json_normalize
import json
import sys
#sys.path.append('../utils')
#from utils.json_utils import write_json
from time import sleep

def delete_unwanted_values(entry):
    del entry['name_romaji']
    del entry['name_kanji']
    del entry['synopsis']
    del entry['premiered']
    del entry['aired']
    del entry['broadcast']
def process_tags(tags): 
    if not tags:
        return None
    return [tag.split('/')[0] for tag in tags]         
def grab_id(link):
    return link.split('/')[4]
def process_staff_data(staff_data):
    if not staff_data:
        return
    for entry in staff_data:
        id = grab_id( entry ['url'])
        entry['id']=id
        del entry['name']
        del entry['url']
def process_studio(studio):
    if studio is None:
        return None
    return studio.split('/')[0]
def parse_duration(duration):
    unit_conversions = {'hr':60,'min':1,'sec':1/60}
    duration_list = duration.split('.')
    duration_minutes = 0
    for val in duration_list:
        val = val.strip()
        if 'ep' in val or not val:
            continue
        else:
            print(val)
            num,units = val.split(' ')
            duration_minutes += int(num) *unit_conversions[units]
    return duration_minutes
    
def write_json(json_dict,output_file):
    with open(output_file, 'w') as fp:
        json.dump(json_dict, fp)
def process_character_data(character_data):
    if not character_data:
        return
    for entry in character_data:
        id = grab_id( entry ['url'])
        entry['id']=id
        del entry['name']
        del entry['url']
def process_entries(data):
    for entry in data:
        delete_unwanted_values(entry)
        process_character_data(entry["char_info"])
        process_staff_data(entry["staff_info"])
        entry['tags '] = process_tags(entry['tags '])
        entry['studio'] = process_studio( entry ['studio'])
        
def start():
    data = json.load(open('results.json','rb'))
    process_entries(data)
    write_json(data,'results2.json')
#start()
s1 = "1 hr. 41 min."
print(parse_duration(s1))
# df = pd.read_json('results.json')
# df = json_normalize(data)
# print(df)
