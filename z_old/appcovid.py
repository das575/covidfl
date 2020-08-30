import os, datetime, time, json, zipfile
import requests
import urllib.parse

from pathlib import Path
from zipfile import ZipFile
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///county_data.db")

response = requests.get("https://www.arcgis.com/sharing/rest/content/items/9512c94d4bea44c488aa86eddfe3b8c1/data")
# requests.get('https://covid19-usflibrary.hub.arcgis.com/datasets/florida-covid19-07182020-bycounty.zip')
response.raise_for_status()

# # Create a ZipFile Object and load the zipped file
# with ZipFile(response, 'r') as zipObj:
#   # Get a list of all archived file names from the zip
#   listOfFileNames = zipObj.namelist()
#   # Iterate over the file names
#   for fileName in listOfFileNames:
#       # Check filename endswith csv
#       if fileName.endswith('.csv'):
#           # Extract a single file from zip
#           zipObj.extract(fileName, 'temp_csv')

p = Path.cwd()
zip = zipfile.ZipFile(p / response)
print(zip.namelist())