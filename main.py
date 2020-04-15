from flask import *
from flask_pymongo import *
from datetime import *
from werkzeug.utils import secure_filename
# import pandas as pd
import csv
import os
app = Flask(__name__)
app.secret_key = "SECRET_KEY"
wsgi_app = app.wsgi_app

# app.config["MONGO_URI"] = "mongodb+srv://evenuss:arjuna203@cluster0-sxt0m.gcp.mongodb.net/contoso"
app.config["MONGO_URI"] = "mongodb://localhost:27017/eventwk"
mongo = PyMongo(app)

UPLOAD_FOLDER = './static/img'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




