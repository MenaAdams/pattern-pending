from model import db, User, Category, User_Category, Project
from flask import flash, session, request
import os
import api

class Pattern:
    url = 'https://www.ravelry.com/patterns/library/'

    def __init__(self, pattern_id):
        pattern_info = api.get_pattern_by_id(pattern_id)
        self.name = pattern_info['name']
        self.pattern_id = pattern_id
        self.permalink = pattern_info['permalink']
        self.url = self.url + self.permalink
        self.photo = pattern_info['photos'][0]['medium2_url']

    def to_dict(self):
        """ Return a dictionary representation of a pattern. """

        return {
                "name": self.name,
                "pattern_id": self.pattern_id,
                "url": self.url,
                "photo": self.photo
            } 


class Project(Pattern):

    def __init__(self, name, pattern_id, link, photo):
        self.name = name
        self.pattern_id = pattern_id
        self.url = link
        self.photo = photo


class Yarn():

    def __init__(self, yarn_line, yarn_brand, yarn_weight):
        self.name = f'{yarn_brand} {yarn_line}' 
        self.weight = yarn_weight.lower()
    
    def to_dict(self):
        """ Return a dictionary representation of a pattern. """

        return {
                "name": self.name,
                "weight": self.weight
            } 

def save_users_rav_data(username):
    """ Adds patterns in users queue, favorites, and library to database. """
    user = User.query.filter_by(ravelry_un=username).first()
    user_patts = {
                'fav': api.get_user_favs(username), 
                'que': api.get_user_queue(username), 
                'lib': api.get_user_library(username)
                }  
    for category_code, patterns in user_patts.items():
        for pattern_id in patterns:
            db.session.add(User_Category(category_code=category_code,
                                    pattern_id=pattern_id,
                                    user=user))


def sort_pattern_type(pattern_id):
    """ Sort default ravelry pattern types into broader categories for database purposes. """ 

    parent_types = {
        'Socks': 'Socks',
        'Hands': 'Gloves and Mittens',
        'Sweater': 'Sweaters',
        'Hat': 'Hat',
        'Softies': 'Plushies'
    }
    pattern_types = {
        'Scarf': 'Scarves and Cowls',
        'Cowl': 'Scarves and Cowls',
        'Shawl / Wrap': 'Shawls and Wraps',
        'Blanket': 'Blankets' 
    }

    pattern = api.get_pattern_by_id(pattern_id)
    pattern_type = pattern['pattern_categories'][0]['name']
    parent_type = pattern['pattern_categories'][0]['parent']['name']

    if parent_type in parent_types:
        return parent_types[parent_type]

    if pattern_type in pattern_types:
        return pattern_types[pattern_type]

    else:
        return 'Other'


def save_projects_to_db(username):
    """ Adds user's completed projects to db. """
    user = User.query.filter_by(ravelry_un=username).first()
    projects = api.get_user_projects(username)
    for project in projects:
        rav_project_id = project['id']
        pattern_id = project['pattern_id']
        if pattern_id and project['status_name']:
            completion_status = project['status_name']
            pattern = api.get_pattern_by_id(pattern_id)
            pattern_type = sort_pattern_type(pattern_id)
            proj = Project(
                        user_id=user.user_id,
                        rav_project_id=rav_project_id,
                        pattern_id=pattern_id,
                        pattern_type=pattern_type,
                        completion_status=completion_status,
                        )
            db.session.add(proj)


def check_database_for_user(username):
    """ Checks database for user and adds them if they're not there. """
    user = User.query.filter_by(ravelry_un=username).first()
    session['username'] = username

    if not user:
        user = User(ravelry_un=username)
        db.session.add(user)
        save_users_rav_data(username)
        save_projects_to_db(username)
        db.session.commit()
        flash(f"Added {user.ravelry_un}'s information")

    else:
        flash(f'Retrieving {user.ravelry_un}\'s information...')


def get_user_patterns():
    """ Get user patterns from db. """
    user_patts= {
                'favorites': [result.pattern_id
                    for result in User_Category.query.filter(
                    User.ravelry_un==session['username'], 
                    User_Category.category_code == 'fav').all()],
                'queue': [result.pattern_id
                    for result in User_Category.query.filter(
                    User.ravelry_un==session['username'], 
                    User_Category.category_code == 'que').all()],
                'library': [result.pattern_id
                    for result in User_Category.query.filter(
                    User.ravelry_un==session['username'], 
                    User_Category.category_code == 'lib').all()]
                }

    return user_patts


def get_user_results():
    """ Returns user specific results from session """
    pattern_ids = set()
    user_patts = get_user_patterns()

    for patt in session['search_results']:
        for category in user_patts:
            if patt in user_patts[category]: 
                pattern_ids.add(patt)  

    return list(pattern_ids)


def objectify_projects(projects_results):
    """ Return list of project objects. """
    projects = []

    for result in projects_results:
        try:
            if result['pattern_id'] and result['first_photo']['medium2_url']:
                name = result['pattern_name']
                pattern_id = result['pattern_id']
                photo = result['first_photo']['medium2_url']
                link = result['links']['self']['href']
                project = Project(name, pattern_id, link, photo)
                projects.append(project)
        except TypeError:
            pass

    return projects
    

def search_patterns():
    """ Search ravelry patterns with user's search parameters, returns None. """

    yarn_type = request.args.get('yarn')
    pattern_type = request.args.get('pattern_type')
    search_params = {'craft': 'knitting',
                    'weight': yarn_type, 
                    'pc': pattern_type,
                    }
    search_results = api.search_patterns(search_params) 
    return search_results


def search_projects():
    """ Search projects database and return project objects. """

    yarn_brand = request.args.get('yarn-brand')
    search_type = request.args.get('search-type')
    search_params = {'craft': 'knitting',
                    'query': f'"{yarn_brand}"'}

    projects_results = api.search_projects(search_params)
    projects = objectify_projects(projects_results)

    return projects


def objectify_yarn_stash(yarn_stash):

    yarn_objs = []

    for yarn in yarn_stash:
        yarn_line = yarn['yarn']['name']
        yarn_brand = yarn['yarn']['yarn_company']['name']
        yarn_weight = yarn['yarn']['yarn_weight']['name']
        yarn = Yarn(yarn_line, yarn_brand, yarn_weight)
        yarn_objs.append(yarn)

    return yarn_objs