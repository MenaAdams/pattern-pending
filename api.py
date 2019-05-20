import requests
import os

RAVELRY_USERNAME = os.environ.get('RAVELRY_USERNAME')
RAVELRY_PASSWORD = os.environ.get('RAVELRY_PASSWORD')

BASE_URL = 'https://api.ravelry.com/'

def user_is_valid(username):
    """ Checks if username is valid and returns True if yes, False if no """ 

    response = requests.get((BASE_URL + f"people/{username}.json"),
                            auth=requests.auth.HTTPBasicAuth(RAVELRY_USERNAME, RAVELRY_PASSWORD),
                            )
    if response:
        return True
    return False


def get_from_ravelry(get_type, search_params, response_key):
    """ Takes in string url ending, parameters dict and returns ravelry dict. """

    response = requests.get((BASE_URL + get_type), 
                            auth=requests.auth.HTTPBasicAuth(RAVELRY_USERNAME, RAVELRY_PASSWORD), 
                            params=search_params
                            )

    all_info = response.json()
    processed_info = all_info[response_key]

    return processed_info


def search_rav(search_params):
    """ Return list of pattern ids that match search criteria. """

    search_url = 'patterns/search.json'
    #update search params with large page size to get more data?
    search_results = get_from_ravelry(search_url, search_params, 'patterns')

    search_patts = []

    for result in search_results:   #refactor w/ list comprehension?
        pattern_id = result['id']
        search_patts.append(pattern_id)
    
    return search_patts


def get_user_favs(username):
    """ Returns list of pattern ids favorited by user on ravelry. """

    favs_url = f'people/{username}/favorites/list.json'
    # included page size in params because default is only 50
    favs_results = get_from_ravelry(favs_url, 
                                    {'type':'pattern',
                                    'page_size':100}, 
                                    'favorites')
    fav_patts = []

    for result in favs_results: #refactor w/ list comprehension?
        pattern_id = result['favorited']['id']
        fav_patts.append(pattern_id)

    return fav_patts


def get_user_queue(username):
    """ Returns list of pattern ids queued by user on ravelry. """ 

    que = f'people/{username}/queue/list.json'
    # include large page size in params because default is only 50
    que_results = get_from_ravelry(que, {'page_size':500}, 'queued_projects')
    que_patts = []

    for result in que_results:
        pattern_id = result['pattern_id']
        if pattern_id:
            que_patts.append(pattern_id)

    return que_patts


def get_user_library(username):
    """ Returns list of pattern ids in user's library on ravelry. """

    lib = f'people/{username}/library/search.json'
    lib_results = get_from_ravelry(lib, {}, 'volumes')
    lib_patts = []

    for result in lib_results: #refactor w/ list comprehension?
        pattern_id = result['pattern_id']
        if pattern_id:
            lib_patts.append(pattern_id)

    return lib_patts


def get_pattern_by_id(pattern_id):
    """ Get ravelry pattern object by id from ravelry. """

    show_patt = f'patterns/{pattern_id}.json'
    response = requests.get((BASE_URL + show_patt), 
                            auth=requests.auth.HTTPBasicAuth(RAVELRY_USERNAME, RAVELRY_PASSWORD), 
                            )
    pattern = response.json()

    return pattern['pattern']