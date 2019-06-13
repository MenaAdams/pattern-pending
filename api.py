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

    return True if response else False


def get_from_ravelry(get_type, search_params, response_key):
    """ Takes in string url ending, parameters dict and returns ravelry dict. """

    response = requests.get((BASE_URL + get_type), 
                            auth=requests.auth.HTTPBasicAuth(RAVELRY_USERNAME, RAVELRY_PASSWORD), 
                            params=search_params
                            )
    all_info = response.json()
    processed_info = all_info[response_key]

    return processed_info


def search_patterns(search_params):
    """ Return list of pattern ids that match search criteria. """

    search_url = 'patterns/search.json'
    #update search params with large page size to get more data?
    search_results = get_from_ravelry(search_url, search_params, 'patterns')

    search_patts = [result['id']
                    for result in search_results]
    
    return search_patts


def search_projects(search_params):
    """ Returns list of projects that match criteria """

    projects_url = 'projects/search.json'
    search_results = get_from_ravelry(projects_url, search_params, 'projects')

    return search_results


def get_user_favs(username):
    """ Returns list of pattern ids favorited by user on ravelry. """

    favs_url = f'people/{username}/favorites/list.json'
    # included larger page size in params because default is only 50
    favs_results = get_from_ravelry(favs_url, 
                                    {'type':'pattern',
                                    'page_size':100}, 
                                    'favorites')
    print(favs_results)
    fav_patts = [result['favorited']['id']
                for result in favs_results
                if result['favorited']]

    return fav_patts


def get_user_queue(username):
    """ Returns list of pattern ids queued by user on ravelry. """ 

    que = f'people/{username}/queue/list.json'
    # include large page size in params because default is only 50
    que_results = get_from_ravelry(que, {'page_size':500}, 'queued_projects')
    que_patts = [result['pattern_id']
                for result in que_results
                if result['pattern_id']] #checks if truthy, so we don't add blank items

    return que_patts


def get_user_library(username):
    """ Returns list of pattern ids in user's library on ravelry. """

    lib = f'people/{username}/library/search.json'
    lib_results = get_from_ravelry(lib, {}, 'volumes')
    lib_patts = [result['pattern_id']
                for result in lib_results
                if result['pattern_id']] #checks if truthy, so we don't add blank items

    return lib_patts


def get_pattern_by_id(pattern_id):
    """ Get ravelry pattern object by id from ravelry. """

    show_patt = f'patterns/{pattern_id}.json'
    response = requests.get((BASE_URL + show_patt), 
                            auth=requests.auth.HTTPBasicAuth(RAVELRY_USERNAME, RAVELRY_PASSWORD), 
                            )
    pattern = response.json()

    return pattern['pattern']


def get_user_projects(username):
    """ Return all of the user's projects. """

    show_projects = f'projects/{username}/list.json'
    projects_results = get_from_ravelry(show_projects, {}, 'projects')

    return projects_results


def get_user_stash(username):
    """ Get yarn names and weights in user's yarn stash"""

    search_yarn = f'people/{username}/stash/list.json'
    yarn_results = get_from_ravelry(search_yarn, {'sort':'recent'}, 'stash')

    return yarn_results
