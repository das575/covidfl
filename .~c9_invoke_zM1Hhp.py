# This successfully downloaded the data from mbevand's files on Github. the problem is that there is no standard name for his files, and he's not always updating it frequently.

import os, datetime, time, json, csv, statistics, zipfile
from pathlib import Path
import requests
import urllib.request
import pandas as pd
import numpy as np
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

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

# # Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///covidfl.db")

# Function to get the string for the date that goes into the USF URL
def date_set(month, day, year):
    # This runs through the dates
    mo_str = "0" + str(month)
    if dy < 10:
        dy_str = "0" + str(day)
    else:
        dy_str = str(dy)

    yr_str = str(yr)
    date_str = mo_str + dy_str + yr_str
    return(date_str)

# Function to convert the dates to a number for computation
def date_ordinal(date):
    # date has to be a string
    date_ord = datetime.datetime.strptime(date, "%x").toordinal()
    return(date_ord)

# Function to subtract the items in the list from one another
def list_subtract(list1, list2):
    list_dfc = []
    list1_len = len(list1)
    list2_len = len(list2)
    if list1_len != list2_len:
        print("Lists must have the same number of items")
    for i in range(list1_len):
        list_dfc.append(list1[i] - list2[i])
    return(list_dfc)

# Function to add the items in the list to one another (adding two lists - used for Tampa region)
def list_add2(list1, list2):
    list_add = []
    list1_len = len(list1)
    list2_len = len(list2)
    if list1_len != list2_len:
        print("Lists must have the same number of items")
    for i in range(list1_len):
        list_add.append(list1[i] + list2[i])
    return(list_add)

# Function to add the items in the list to one another (adding two lists - used for Tampa region)
def list_add3(list1, list2, list3):
    list_add = []
    list1_len = len(list1)
    list2_len = len(list2)
    list3_len = len(list3)
    if list1_len != list2_len:
        print("Lists must have the same number of items")
    if list1_len != list3_len:
        print("Lists must have the same number of items")
    for i in range(list1_len):
        list_add.append(list1[i] + list2[i] + list3[i])
    return(list_add)

# Function to determine the right region
def region(county):
    if county == 'Collier':
        region = 'Collier'
    elif county == 'Lee':
        region = 'Lee'
    elif county == 'Dade' or county == 'Broward' or county == 'Palm Beach':
        region = 'South Florida'
    elif county == 'Hillsborough' or county == 'Pinellas':
        region = 'Tampa Bay Region'
    elif county == 'Orange' or county == 'Polk' or county == 'Osceola':
        region = 'Orlando Region'
    elif county == 'Duval' or county == 'St. Johns':
        region = 'Jacksonville Region'
    elif county == 'State':
        region = 'State'
    else:
        region = 'Rest of Florida'
    return(region)

date_list = []
startDate = '07282020'

start = datetime.datetime.strptime(startDate, '%m%d%Y')
end = datetime.datetime.today() - datetime.timedelta(days=1)
days_iter = end.toordinal() - start.toordinal()

# Iterate over the days
for dayNum in range(0, days_iter + 1):
    date = start + datetime.timedelta(days=dayNum)
    date_str = datetime.datetime.strftime(date, '%m%d%Y')
    # print(date_str)
    date_f = date.strftime('%m/%d/%Y')
    # print(date_f)
    date_list.append(date_f)

    # From USF archive of DOH data. These compile stats from CSV. Each file is about 70 rows.
    url_step1 = "https://covid19-usflibrary.hub.arcgis.com/datasets/florida-covid19-" + date_str + "-bycounty-csv"
    url = url_step1

    # Extract the long string from the website that identifies the file name.
    try:
        response = requests.get(url)
        response.raise_for_status()
    except:
        print("Download problem on " + date_f)
    # print(response.text)
    http_code = response.text
    before, sep, after = http_code.partition("https://www.arcgis.com/sharing/rest/content/items/")
    before, sep, after = after.partition("/info")
    csv_loc = before
    # print(before)

    # Get the URL of the CSV data by concatenation
    url = "https://www.arcgis.com/sharing/rest/content/items/" + csv_loc + "/data"

    # response = requests.get(url)
    # response.raise_for_status()
    # print(type(response))
    # cr = csv.reader(response, delimiter=',')
    # print(type(cr))

    # Open the URL, unzip the file, and read in the CSV
    try:
        resp = urlopen(url)
        zipped = ZipFile(BytesIO(resp.read()))
        csv_file = open(zipped.extract('Florida_COVID_Cases_0.csv'))
    except:
        print("Unzip problem on " + date_f)
    csv_read = csv.reader(csv_file)
    csv_data_raw = list(csv_read)
    # This deletes a number of columns that aren't necessary for our purposes
    for j in csv_data_raw:
        del j[0:5]
        del j[78:]
    csv_data = csv_data_raw
    # print("Part 2 = ")
    # print(csv_data[0])

    # Count the rows in the file
    csv_rows = len(csv_data)
    csv_cols = len(csv_data[0])

    # print(csv_cols)
    # print(len(csv_data[1]))
    if csv_data[0][77] != 'Deaths':
        print('Date = ' + date_str)
        print('column 77 = ' + csv_data[0][77])
        print(csv_data[0].index('Deaths'))

    # I've already pre-loaded covidfl.csv with the header row.

    # # Open the main covidfl.csv file and check to see if there's anything there. If it's [], then open the writer as 'w' (and write the . Otherwise, it's 'a'
    # with open('covidfl.csv', mode='r') as covidfl:
    #     covidfl = csv.reader(covidfl.csv, delimiter=',')
    #     covidfl_list = list(covidfl)
    # if covidfl_list == []:

    # Append each row with date_f
    #
###############################This works, but I just want to concentrate on the math of the daily changes
    counties = []
    for i in range(1,csv_rows):
        csv_data[i].append(date_f)
        csv_data[i].append(region(csv_data[i][0]))
        counties.append(csv_data[i][0])
        with open('covidfl.csv', mode='a') as covidfl:
            writer = csv.writer(covidfl, delimiter=',', quotechar="'", quoting=csv.QUOTE_ALL, skipinitialspace=True)
            writer.writerow(csv_data[i])
        covidfl.close()

# print(counties)
# Limit the date list to the final X number of days for iteration
date_count = len(date_list)
x = 4
if x > date_count:
    print("Increase the number of downloaded days")
else:
    date_list_lastx = date_list[-x:]
# Set the maximum date, which will be used on the website to say: "Data Updated as of {date_max}"
date_max = max(date_list)

# Set data_fl file
try:
    data_fl = pd.read_csv('covidfl.csv', delimiter=',', quotechar="'",  header=0)
except:
    print('covidfl.csv file does not exist')

# This goes through the loop to get me the data I'm looking for
# First set an empty list for my web data
# web_lists = ['Region','Date','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative','CasesAll_Chg','C_HospYes_Res_Chg','C_HospYes_NonRes_Chg','Deaths_Chg','T_negative_Chg']
# web_lists_row = 0
region_date_chg = ['Region','Date','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative','CasesAll_Chg','C_HospYes_Res_Chg','C_HospYes_NonRes_Chg','Deaths_Chg','T_negative_Chg']
region_date_chg_row = 0
region_list = ['Collier','Lee','South Florida','Tampa Bay Region','Orlando Region','Jacksonville Region','Rest of Florida','State']

print()
# Get the last date from the database
for date in reversed(date_list_lastx):
    region_date_chg_row += 1
    # date_list = set(data_fl['Date'].tolist())
    # date_last_str = max(date_list_lastx)
    date_last_str = date
    date_prior = datetime.datetime.strptime(date_last_str, '%m/%d/%Y') - datetime.timedelta(days=1)
    date_prior_str = datetime.datetime.strftime(date_prior, '%m/%d/%Y')
    for region in region_list:

        # date_last_str = '07/31/2020'
        # date_prior_str = '07/30/2020'
        day0_data = data_fl[(data_fl.Region == region) & (data_fl.Date == date_last_str)][['CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].values.tolist()
        day0_data = day0_data[0]
        # print(day0_data)
        day1_data = data_fl[(data_fl.Region == region) & (data_fl.Date == date_prior_str)][['CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].values.tolist()
        day1_data = day1_data[0]
        # print(day1_data)

        region_date_chg.append([region] + [date_last_str] + day0_data + list_subtract(day0_data, day1_data))
print(region_date_chg)
print('Number of rows in region_date_chg: ' + str(len(region_date_chg)))

# TO DO: GET JUST THE LATEST DATE FOR INDEX -- USE date_max variable
region_table_last = []
for row in region_date_chg:
    while row[1] == date_max:
        region_table_last.append(row)
print(region_table_last)

# TO DO: DO THE CALCULATIONS FOR THE 7-DAY MOVING AVERAGE



##### START HERE... I NEED TO FIGURE
# I took this from the application.py from the finance subfolders
@app.route("/")
def index():
    """Show portfolio of stocks"""
    # Initialize the portfolio list
    portfolio_list = []

    # Initialize the symbol_shares list, which will be used for  the table of symbols and sum of shares.
    symbol_shares_list = []

    # The user_id will be used to make sure the database pull is only for the logged in user.
    index_user_id = session["user_id"]

    # Database pull for symbol and sum of shares, filtered where the sum of shares are greater than 0
    symbol_shares_list = db.execute("SELECT symbol, sum(shares) FROM txns WHERE user_id = :id GROUP BY symbol HAVING sum(shares) > 0",
            id=index_user_id)
    stocks_in_port = len(symbol_shares_list)

    # Set up the components that will go in the HTML table.
    stock_value = 0.0
    if stocks_in_port > 0:
        for i in range(stocks_in_port):
            # Initialize the list as list of lists with None
            portfolio_list.append([None] * 6)
            # Data item #1 is symbol
            portfolio_list[i][0] = symbol_shares_list[i]["symbol"]
            # Data item #3 is sum of the shares
            portfolio_list[i][2] = symbol_shares_list[i]["sum(shares)"]
            # Use IEX lookup for #2, 4, and 5
            iex_lookup = lookup(symbol_shares_list[i]["symbol"])
            # Data item #2 is name of the stock
            portfolio_list[i][1] = iex_lookup["name"]
            # Data item #4 is name of the stock
            portfolio_list[i][3] = usd(iex_lookup["price"])
            # Data item #5 is the current value of the stock (price x current total shares)
            portfolio_list[i][4] = iex_lookup["price"] * symbol_shares_list[i]["sum(shares)"]
            # Data item #6 is the string representation of Data item #5 (current stock value)
            portfolio_list[i][5] = usd(portfolio_list[i][4])
            # This updates the total stock value with Data item #5 (current stock value)
            stock_value = stock_value + float(portfolio_list[i][4])
        # print(portfolio_list)
        # print("Stocks total = " + usd(stock_value))

    # Database pull in order to get the cash from the logged in user
    rows = db.execute("SELECT cash FROM users WHERE id = :id",
              id=index_user_id)
    cash = rows[0]["cash"]
    # print("Cash total = " + usd(cash))
    port_value = stock_value + cash
    # print("Grand total = " + usd(port_value))
    # Get the number of rows in the portfolio, which will be used in the index table
    rows = len(portfolio_list)
    # print("rows for portfolio = " + str(rows))
    return render_template("index.html", portfolio_list=portfolio_list, stock_value=usd(stock_value), cash=usd(cash), port_value=usd(port_value), rows=rows)