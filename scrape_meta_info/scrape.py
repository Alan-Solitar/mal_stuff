import requests
from bs4 import BeautifulSoup
from time import sleep
import json
#urls
#'https://jikan.me/api/anime/{mal_id}/characters_staff'
character_staff_url = 'https://jikan.me/api/anime/{}/characters_staff'
generic_endpoint = 'https://myanimelist.net/malappinfo.php?u={}&status={}&type=anime'
mal_url = 'https://myanimelist.net/anime/{}'

#vars
username = input('username:')
status = 'all'

def grab_list(username='',status='all'):
    if not username:
        return None
    endpoint = generic_endpoint.format(username,status)
    xml = requests.get(endpoint).text
    return xml
def parse_list(xml):
    if not xml:
        return
    parser = BeautifulSoup(xml,'xml')
    list_entries = parser.findAll('anime')
    anime_details_list = []
    i = 0
    failed_counter = 0
    for entry in list_entries:
        i+=1
        try:
            db_id = entry.find('series_animedb_id').text
            series_type = entry.find('series_type').text
            status = entry.find('series_status').text
            score = int(entry.find('my_score').text)
            obj = None
            # if int(status) == 1:
            anime_details = grab_anime_details(db_id)
            anime_details['mal_id'] = db_id
            anime_details['my_score'] =score
            anime_details['series_status'] = status
            anime_details['series_type'] = series_type
            anime_details_list.append(anime_details)
        except:
            print('failed')
            failed_counter+=1
        if i%50 == 0:
            print('{} entries processed'.format(i))
        sleep(1)
    
    write_json(anime_details_list)
    print("{}suceeded and {} failed".format(i-failed_counter,failed_counter))
def grab_anime_details(db_id):
    resp = requests.get(character_staff_url.format(db_id))
    json_dict = json.loads(resp.text)
    return parse_json_response(json_dict)
def parse_json_response(json_dict):
    
        return {
            
            'name_kanji':json_dict.get('japanese'),
            'name_romaji':json_dict.get('title'),
            'score':json_dict.get('score')[0],
            'studio': json_dict.get('studio')[0][1],
            'tags ': parse_tags(json_dict.get('genre')),
            'duration' : json_dict.get('duration'),
            'char_info' : parse_characters(json_dict.get('character')),
            'staff_info' : parse_staff(json_dict.get('staff')),
            'source' : json_dict.get('source'),
            'synopsis':json_dict.get('synopsis'),
            'status':json_dict.get('status'),
            'episodes':json_dict.get('episodes'),
            'media_format':  json_dict.get('type'),
            'broadcast':json_dict.get('broadcast'),
            'aired':json_dict.get('aired'),
            'premiered':json_dict.get('premiered'),
        }
    
def parse_tags(tags):
    if not tags:
        return None
    return [tag[1] for tag in tags]
def parse_characters(characters):
    if not characters:
        return None
    char_info = []
    for char in characters:
        role = char['role']
        voice_actors = char['voice-actor']
        for actor in voice_actors:
            if actor['role']=='Japanese':
                url = actor['url']
                name = actor['name']
                char_info.append({'url':url,'name':name,'role':role})
    return char_info
def parse_staff(staff):
    if not staff:
        return None
    staff_info = []
    
    for staff_member in staff:
        url = staff_member['url']
        name = staff_member['name']
        role = staff_member['role']
        staff_info.append({'url':url,'name':name,'role':role})
    return staff_info
def run_list_parser():
    xml = grab_list(username=username,status='all')
    parse_list(xml)
def write_json(json_dict):
    with open('results.json', 'w') as fp:
        json.dump(json_dict, fp)
def run():
    run_list_parser()
run()