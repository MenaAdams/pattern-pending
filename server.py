#!/usr/bin/env python
import os

import requests
import api
import random
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Category, User_Category, Project

app = Flask(__name__)
app.secret_key = "G59Q#m$HWvhMYs#Kuw#nT7eeKF%@ofoBhUBz4MZrF0UUvN5s#*8CB4l!B#Uz9Ob@xW4m#8VRf88"

RAVELRY_USERNAME = os.environ.get('RAVELRY_USERNAME')
RAVELRY_PASSWORD = os.environ.get('RAVELRY_PASSWORD')

class Pattern:
    url = 'https://www.ravelry.com/patterns/library/'

    def __init__(self, pattern_id):
        pattern_info = api.get_pattern_by_id(pattern_id)
        self.name = pattern_info['name']
        self.pattern_id = pattern_id
        self.permalink = pattern_info['permalink']
        self.url = self.url + self.permalink
        self.photo = pattern_info['photos'][0]['medium2_url']


def save_users_rav_data(username):
    """ Adds patterns in users queue, favorites, and library to database. """
    user = User.query.filter_by(ravelry_un=username).first()
    user_patts = {
                'fav': api.get_user_favs(username), 
                'que': api.get_user_queue(username), 
                'lib': api.get_user_library(username)
                }  
    for category_code in user_patts:
        for pattern_id in user_patts[category_code]:
            pattern = User_Category(category_code=category_code,
                                    pattern_id=pattern_id,
                                    user_id=user.user_id)
            db.session.add(pattern)


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
            pattern_type = pattern['pattern_categories'][0]['name']
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

    if not user:
        user = User(ravelry_un=username)
        db.session.add(user)
        save_users_rav_data(username)
        save_projects_to_db(username)
        db.session.commit()
        flash(f"Added {user.ravelry_un}'s information")

    else:
        flash(f'Retrieving {user.ravelry_un}\'s information...')

    session['username'] = user.ravelry_un


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


@app.route("/") 
def homepage():
    """ Render homepage. """

    return render_template('homepage.html')


@app.route("/rav-data", methods=['POST'])
def get_users_rav_data():
    """ Grab user's personal ravelry data. """
    username = request.form.get('username')
    username = username.lower()

    if api.user_is_valid(username): 
        check_database_for_user(username)
        return redirect('/search')

    else:
        flash(f'"{username}" is not a valid ravelry account. Please try again.')
        return redirect('/')


@app.route("/users-categories.json")
def jsonify_user_patterns():
    """ Returns jsonified user_patts. """
    user_patts = get_user_patterns()

    return jsonify(user_patts)


@app.route("/search")
def render_search_page():
    """ Display search page to get user search criteria. """

    return render_template('search.html')


@app.route("/search-data")
def get_search_criteria():
    """ Save user's search inputs to session. """
    
    yarn_type = request.args.get('yarn')
    pattern_type = request.args.get('pattern_type')
    search_params = {'craft': 'knitting',
                    'weight': yarn_type, 
                    'pc': pattern_type,
                    }
    search_results = api.search_rav(search_params) 
    session['search_results'] = search_results

    return redirect('/search-rav') 


def get_user_results():
    """ Returns user specific results from session """
    pattern_ids = set()
    user_patts = get_user_patterns()

    for patt in session['search_results']:
        for category in user_patts:
            if patt in user_patts[category]: 
                pattern_ids.add(patt)  

    return pattern_ids


@app.route("/search-rav")
def display_search_rav():
    """ Display random search results plus user relevant patterns. """
    pattern_ids = set(random.choices(session['search_results'], k=6))
    pattern_ids.update(get_user_results())
    user_patts = get_user_patterns()
            
    patterns = [Pattern(patt) 
                for patt in pattern_ids]

    return render_template('search-results.html', 
                            patterns=patterns, 
                            user_patts=user_patts)


if __name__ == "__main__":
    app.debug=True
    connect_to_db(app)
    app.run(host="0.0.0.0")
    DebugToolbarExtension(app)
