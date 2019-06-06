#!/usr/bin/env python
import os
import requests
import api
import random
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Category, User_Category, Project
from ravelry import (Pattern, save_users_rav_data, sort_pattern_type, save_projects_to_db,
    check_database_for_user, get_user_patterns, get_user_results, search_patterns,
    search_projects)


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
    search_type = request.args.get('search-type')
    print("search type is", search_type)

    if search_type == 'pattern':
        search_results = search_patterns()
    elif search_type == 'project':
        search_results = search_projects()
        search_results = [result.to_dict() for result in search_results]

        print("project search results")
        #projects are already objects
    session['search_results'] = search_results
    print(session['search_results'])
    print('search results saved to session=============================')
    session['search_type'] = search_type

    return redirect('/search-rav') 


# @app.route('/search-projects')
# def search_projects():
#     """ """
#     yarn_brand = request.args.get('yarn-brand')
#     search_type = request.args.get('search-type')
#     print(search_type,  "is search_type")
#     print(yarn_brand, "is yarn brand")
#     search_params = {'craft': 'knitting',
#                     'query': f'"{yarn_brand}"'}
#     print(search_params)
#     projects_results = api.search_projects(search_params)
#     projects = parse_project_search(projects_results)

#     return render_template('search-results.html', patterns=projects)


@app.route("/search-rav")
def display_search_rav():
    """ Display search results page.
    React component on html page """
    print('rendering search results')
    return render_template('search-results.html')


@app.route('/search-results.json')
def jsonify_pattern_search():
    """ Display random search results plus user relevant patterns. """
    print('in search-results.json function =================')
    if session['search_type'] == 'pattern':
        pattern_ids = set(random.choices(session['search_results'], k=6)) #used a set to easily eliminate duplicate results
        pattern_ids.update(get_user_results()) #maybe only add up to a limited number?
        user_patts = get_user_patterns()
        patterns = [Pattern(patt) 
                    for patt in pattern_ids]
        patterns = [pattern.to_dict() for pattern in patterns]
    else:
        print('search results json function')
        print("search results--------------", session['search_results'])
        patterns = random.choices(session['search_results'], k=6)
        print("patterns-----------------------", patterns)
        #how to add user patts?

    return jsonify(patterns)


@app.route('/search-projects.json')
def jsonify_project_search():
    """sdf """

    pattern_selections = set(random.choices(session['search_results'], k=6))
    #how to add user patts?
    return jsonify([pattern.to_dict() for pattern in pattern_selections])


@app.route('/pattern-types.json')
def get_pattern_types_data():
    """Return data about User's projets ."""
    user = User.query.filter_by(ravelry_un=session['username']).first()
    sums, total = user.calculate_project_stats() #([(pattern_type, sum),...], total)
    colors = ['#FFDAD6', '#F3E8B4', '#B9E795', '#79DC95', 
            '#5ECED0', '#4666C4', '#7130B9', '#AD1C85', '#A10A13']
    
    data_dict = {
                "labels": [sum[0]for sum in sums],
                "datasets": [
                    {
                        "data": [int((sum[1]/total) * 100) for sum in sums],
                        "backgroundColor": colors[:len(sums)],
                        "hoverBackgroundColor": colors[:len(sums)]
                    }]
            }

    return jsonify(data_dict)


@app.route('/completion-status.json')
def get_completion_status_data():
    """Return data about User's projets ."""
    user = User.query.filter_by(ravelry_un=session['username']).first()
    sums, total = user.calculate_project_status_stats() #([(completion_status, sum),...], total)
    colors = ['#A10A13', '#79DC95', '#4666C4', '#FFDAD6']
    
    data_dict = {
                "labels": [sum[0]for sum in sums],
                "datasets": [
                    {
                        "data": [int((sum[1]/total) * 100) for sum in sums],
                        "backgroundColor": colors[:len(sums)],
                        "hoverBackgroundColor": colors[:len(sums)]
                    }]
            }

    return jsonify(data_dict)   

@app.route('/user')
def display_user_charts():

    return render_template('userpage.html')





if __name__ == "__main__":
    app.debug=True
    connect_to_db(app)
    app.run(host="0.0.0.0")
    DebugToolbarExtension(app)
