#!/usr/bin/env python
import os

import requests
import api
import random
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

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
        self.photos = []
        for photo in pattern_info['photos']:
            self.photos.append(photo['medium2_url'])


@app.route("/")
def homepage():
    """ Render homepage. """

    return render_template('homepage.html')

@app.route("/rav-data")
def get_users_rav_data():
    """ Grab user's personal ravelry data. """
    username = request.args.get('username')

    if api.user_is_valid(username):
        user_patts = {
                    'favorites': api.get_user_favs(username), 
                    'queue': api.get_user_queue(username), 
                    'library': api.get_user_library(username)
                    }
        session['user_patts'] = user_patts
        print(session['user_patts'])
        return redirect('/search')

    else:
        flash(f'"{username}" is not a valid ravelry account. Please try again.')
        return redirect('/')


@app.route("/search")
def render_search_page():
    """ Display search page to get user search criteria. """
    print('your search page!!!!')
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
    print('search params', search_params)
    search_results = api.search_rav(search_params) 
    print('your searchresults=', search_results)
    session['search_results'] = search_results
    print('got your search results -----------------------------------------')

    return redirect('/search-rav') 


@app.route("/search-rav")
def display_search_rav():
    """ Display random search results plus user relevant patterns. """
    pattern_ids = random.choices(session['search_results'], k=6)

    for key in session['user_patts'].keys():
        for patt in session['search_results']:
            if patt in session['user_patts'][key]: 
                if not patt in pattern_ids:
                    pattern_ids.insert(0, patt)
            
    patterns = []
    for patt in pattern_ids:
        patt = Pattern(patt)
        patterns.append(patt)

    return render_template('search-results.html', patterns=patterns)

if __name__ == "__main__":
    app.debug=True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.run(host="0.0.0.0")
    DebugToolbarExtension(app)
