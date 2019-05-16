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

    return render_template('homepage.html')



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
