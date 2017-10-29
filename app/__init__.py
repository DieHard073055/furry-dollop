# @file         __init__.py
# @description  initializes the flask application
#               imports the files views.py and prng.py
# @author       Eshan Shafeeq
from flask import Flask

app = Flask(__name__)
from app import views
from app import prng
