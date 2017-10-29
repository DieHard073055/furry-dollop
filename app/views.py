# @file         views.py
# @description  will handle the request to /index and /
# @author       Eshan Shafeeq

from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

