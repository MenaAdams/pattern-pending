#!/usr/bin/env python
import os
import requests
import api
import random
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Category, User_Category, Project
from ravelry import (Pattern, save_users_rav_data, sort_pattern_type, save_projects_to_db,
    check_database_for_user, get_user_patterns)


app = Flask(__name__)
app.secret_key = "G59Q#m$HWvhMYs#Kuw#nT7eeKF%@ofoBhUBz4MZrF0UUvN5s#*8CB4l!B#Uz9Ob@xW4m#8VRf88"

RAVELRY_USERNAME = os.environ.get('RAVELRY_USERNAME')
RAVELRY_PASSWORD = os.environ.get('RAVELRY_PASSWORD')


@app.route('/') 
def homepage():
    """ Render homepage. """

    return render_template('homepage.html')


@app.route('/rav-data', methods=['POST'])
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


@app.route('/users-categories.json')
def jsonify_user_patterns():
    """ Returns jsonified user_patts. """
    user_patts = get_user_patterns()

    return jsonify(user_patts)


@app.route('/search')
def render_search_page():
    """ Display search page to get user search criteria. """

    return render_template('search.html')


@app.route('/search-data')
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

@app.route('/pattern-types.json')
def pattern_types_data():
    """Return data about User's projets ."""
    user = User.query.filter_by(ravelry_un=session['username']).first()
    sums, total = user.calculate_project_stats() #([(pattern_type, sum)...], (username, total)
    colors = ['#FFDAD6', '#F3E8B4', '#B9E795', '#79DC95', '#5ECED0', '#4666C4', '#7130B9', '#AD1C85', '#A10A13']
    
    data_dict = {
                "labels": [sum[0]for sum in sums],
                "datasets": [
                    {
                        "data": [(sum[1]/total[1])*10 for sum in sums],
                        "backgroundColor": colors[:len(sums)],
                        "hoverBackgroundColor": colors[:len(sums)]
                    }]
            }

    return jsonify(data_dict)

@app.route('/user')
def display_user_charts():

    return render_template('userpage.html')


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
