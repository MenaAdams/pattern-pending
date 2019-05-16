#!/usr/bin/env python
# from pprint import pformat
import os

import requests
import api
from flask import Flask, render_template, request, flash, redirect
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret_key = "G59Q#m$HWvhMYs#Kuw#nT7eeKF%@ofoBhUBz4MZrF0UUvN5s#*8CB4l!B#Uz9Ob@xW4m#8VRf88"

RAVELRY_USERNAME = os.environ.get('RAVELRY_USERNAME')
RAVELRY_PASSWORD = os.environ.get('RAVELRY_PASSWORD')

@app.route("/")
def homepage():
    """ Render homepage. """

    return render_template('homepage.html')

@app.route("/rav-data")
def get_users_rav_data():
    """ Grab user's personal ravelry data"""
    username = request.args.get('username')

    if api.user_is_valid(username):
        user_patts = {}
        user_data_functions = [api.get_user_favs(username),
                            api.get_user_queue(username),
                            api.get_user_library(username)]
        #loop through patterns in users favs, queue, library
        #count how many times pattern appears
        for funct in user_data_functions:
            patts = funct
            print(patts)
            for patt in patts:
                if user_patts.get('patt'):
                    user_patts[patt] += 1
                else:
                    user_patts[patt] = 1
        print(user_patts, "=========user_patts==========")
        return render_template('user.html',
                                # user_patts = user_patts,
                                )
    else:
        flash(f'"{username}" is not a valid ravelry account. Please try again.')
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
