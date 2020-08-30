# This successfully downloaded the data from mbevand's files on Github. the problem is that there is no standard name for his files, and he's not always updating it frequently.

import os, datetime, time, json, csv, statistics
import requests
import urllib.request

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# from helpers import apology, login_required, lookup, usd # FROM CS50 FINANCE

# THIS WORKED, BUT IT'S VERY TIME CONSUMING SINCE IT BRINGS IN THE DATA AT THE CASE FILE LEVEL. THERE ARE OVER 360k RECORDS, AND IT ONLY PERMITS 2,000 RECORDS AT A TIME

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
db = SQL("sqlite:///covidfl.db")

# From github mbevand with csvs of the historic case line data
url_7 = "https://github.com/mbevand/florida-covid19-line-list-data/raw/master/data_fdoh/2020-07-22-08-30-29.csv"
url = url_7
# url_8 = flcv19test.csv


# This is the temp DictReader using the sample CSV
# cr = csv.DictReader(open("flcv19test.csv", "r"))

# This is the DictReader using the URL
response = urllib.request.urlopen(url)
lines = [l.decode('utf-8-sig') for l in response.readlines()]
# response = requests.get(url)
# lines = [l.decode('utf-8') for l in response.readlines()]
cr = csv.DictReader(lines, delimiter=',')
fields = cr.fieldnames

print(fields)
all_age_list = list()
hosp_age_list = list()
died_age_list = list()
case = 0
hosp = 0
died = 0

for row in cr:
    if row['County'] == "Collier":
        case += 1
        all_age_list.append(row['Age'])
        if row['Hospitalized'].lower() == "yes":
            hosp += 1
            hosp_age_list.append(row['Age'])
        if row['Died'].lower() == "yes":
            died += 1
            died_age_list.append(row['Age'])

print("Cases = " + str(case))
print("Hospitalizations = " + str(hosp))
print("Died = " + str(died))
print("Median Age " + str(statistics.median(all_age_list)))
print("Median Age of Hospitalizations" + str(statistics.median(hosp_age_list)))
print("Median Age of Died" + str(statistics.median(died_age_list)))