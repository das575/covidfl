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

# Function to subtract the items in the list from one another. This is used to calculate the daily changes
def list_subtract(list1, list2):
    list_dfc = []
    list1_len = len(list1)
    list2_len = len(list2)
    if list1_len != list2_len:
        print("Lists must have the same number of items")
    for i in range(list1_len):
        list_dfc.append(list1[i] - list2[i])
    return(list_dfc)

# Function to add the items in the list to one another (adding two lists - used for Jacksonville region)
def list_add2(list1, list2):
    list_add = []
    list1_len = len(list1)
    list2_len = len(list2)
    if list1_len != list2_len:
        print("Lists must have the same number of items")
    for i in range(list1_len):
        list_add.append(list1[i] + list2[i])
    return(list_add)

# Function to add the items in the list to one another (adding two lists - used for Tampa, South Florida, and Orlando regions)
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

# Check to see that covidfl.csv exists.
try:
    data_fl = pd.read_csv('covidfl.csv', delimiter=',', quotechar="'",  header=0)
except:
    print('covidfl.csv file does not exist')

date_max_csv = data_fl['Date'].max()
print('\nDATE_MAX_CSV: ',date_max_csv)

# Initialize the date list
date_list = list(data_fl['Date'].unique())
print('\nDATE_LIST: ',date_list)

start = datetime.datetime.strptime(date_max_csv, '%m/%d/%Y') + datetime.timedelta(days=1)
print('\nSTART: ',start)

# If the CSV file is already updated to today, then skip all the dating information. CAREFUL:
if datetime.datetime.strptime(date_max_csv, '%m/%d/%Y').date() != datetime.date.today():
    end = datetime.date.today() - datetime.timedelta(days=1)
    # end = datetime.datetime.strptime('08062020', '%m%d%Y')
    days_iter = end.toordinal() - start.toordinal()
else:
    days_iter = 0

# Iterate over the days from start to end
for dayNum in range(0, days_iter + 1):
    date = start + datetime.timedelta(days=dayNum)
    date_str = datetime.datetime.strftime(date, '%m%d%Y')
    print('\nDATE_STR: ',date_str)
    # Format the date appropriately
    date_f = date.strftime('%m/%d/%Y')
    # Add each date to date_list
    date_list.append(date_f)

    # From USF archive of DOH data. These compile stats from CSV. Each file is about 70 rows.
    url_step1 = "https://covid19-usflibrary.hub.arcgis.com/datasets/florida-covid19-" + date_str + "-bycounty-csv"
    url = url_step1

##########################################################################################################
# CHECK FOR ZIP FILE OR CSV FILE
#########################################################################################################

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

    # Open the URL, unzip the file, and read in the CSV
    try:
        resp = urlopen(url)
        zipped = ZipFile(BytesIO(resp.read()))
        csv_file = open(zipped.extract('Florida_COVID_Cases_0.csv'))
    except:
        csv_down = requests.get(url)
        csv_down.raise_for_status()
        csv_file = open('Florida_COVID_Cases_0.csv')
    else:
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
    # Write each line from the USF data to a row in covidfl.csv file
    counties = []
    for i in range(1,csv_rows):
        # Add the appropriate date to the end of each row
        csv_data[i].append(date_f)
        # Add the region to the end of each row
        csv_data[i].append(region(csv_data[i][0]))
        counties.append(csv_data[i][0])
        with open('covidfl.csv', mode='a') as covidfl:
            writer = csv.writer(covidfl, delimiter=',', quotechar="'", quoting=csv.QUOTE_ALL, skipinitialspace=True)
            writer.writerow(csv_data[i])
        covidfl.close()

# print(counties)
# Limit the date list to the final X number of days for iteration
date_count = len(date_list)
x = 7

if x > date_count:
    print("Increase the number of downloaded days")
else:
    date_list_lastx = date_list[-x:]

print('\nDATE_LIST: ',date_list)
print('\nDATE_LIST_LASTX: ',date_list_lastx)

# Set the maximum date, which will be used on the website to say: "Data Updated as of {date_max}"
date_max = max(date_list)

# Header for the table that will contain the core data that will then be extracted to strings for HTML.
region_date_chg = [['Region','Date','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative','CasesAll_Chg','C_HospYes_Res_Chg','C_HospYes_NonRes_Chg','Deaths_Chg','T_negative_Chg']]

# Initialize the # of rows
region_date_chg_row = 0

# Region list that we will iterate over in order to create the rows.
region_list = ['Collier','Lee','South Florida','Tampa Bay Region','Orlando Region','Jacksonville Region','Rest of Florida','State']

# Header for the table that will be sent to the HTML code
region_table_html = [['Region', 'Date', 'CasesToday', 'HospToday', 'DeathsToday', 'TestsToday', 'PctPosToday', 'Cases7Day', 'Hosp7Day', 'Deaths7Day', 'Tests7Day', 'PctPos7Day']]

# Update data_fl for the new days
data_fl = pd.read_csv('covidfl.csv', delimiter=',', quotechar="'",  header=0)

# Get the last date from the database
for date in reversed(date_list_lastx):
    region_date_chg_row += 1
    # date_list = set(data_fl['Date'].tolist())
    # date_last_str = max(date_list_lastx)
    date_last_str = date
    date_prior = datetime.datetime.strptime(date_last_str, '%m/%d/%Y') - datetime.timedelta(days=1)
    date_prior_str = datetime.datetime.strftime(date_prior, '%m/%d/%Y')
    print('\nDATE_LAST_STR: ',date_last_str)
    print('\nDATE_PRIOR_STR: ',date_prior_str)
    for region in region_list:

        # Panda pull of data by region and date(x)
        day0_data = data_fl[(data_fl.Region == region) & (data_fl.Date == date_last_str)][['Region','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].groupby('Region').sum()
        day0_data = day0_data.values.tolist()
        if region_date_chg_row == 1:
            print('\nREGION: ',region)
            print('DATE_LAST_STR: ',date_last_str)
            print('DAY0_DATA: ',day0_data)
        day0_data = day0_data[0]
        print(day0_data)
        # Panda pull of data by region and date(x -1)
        day1_data = data_fl[(data_fl.Region == region) & (data_fl.Date == date_prior_str)][['Region','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].groupby('Region').sum()
        day1_data = day1_data.values.tolist()
        day1_data = day1_data[0]
        # Append a new list to the list 'region_date_chg' which consists of Region, Date, and then the differences
        print('\nREGION: ',region)
        print('DATE_LAST_STR: ',date_last_str)
        print('DAY0_DATA: ',day0_data)
        print('DAY1_DATA: ',day1_data)
        print('DIFFERENCE: ',list_subtract(day0_data, day1_data))
        region_date_chg.append([region] + [date_last_str] + day0_data + list_subtract(day0_data, day1_data))
print('REGION_DATE_CHG *********************************************')
print(region_date_chg)
print('Number of rows in region_date_chg: ' + str(len(region_date_chg)))
region_table_last = region_date_chg[0:7]
print('REGION_TABLE_LAST *********************************************')
print(region_table_last)


# This is a list of lists of the date and region combinations for the last date. Also need to do the calculations for total tests and % positive
# region_table_last = []
# for i in range(1,len(region_date_chg)-1):
#     if region_date_chg[i][1] == date_max:
#         region_table_last.append(region_date_chg[i])
#     else:
#         break
# print("REGION_TABLE_LAST *******************************")
# print(region_table_last)



##############################################################################################################
# TODO: This runs a Panda which first limits the dates to look at and then gets the X-day average
# Panda pull of fake CSV data and limits by date and then sums totals
# Recall that 'region_list' is our list of regions for iteration
rows = len(region_list)
data_fl = pd.read_csv('covidfl.csv',delimiter=',', quotechar="'")

# List of the dates in our CSV file
# Recall that 'date_list_lastx' represents a list of the last X days for iteration

last_date_panda = data_fl.Date.max()
print('LAST_DATE_PANDA *************************')
print(last_date_panda)
print('DATE_LIST_LASTX *************************')
print(date_list_lastx)

# Find the last day (these will be in sequential order)
date_last_str = date_list_lastx[-1]
print('DATE_LAST_STR *************************')
print(date_last_str)

# Go X days back in time for the start date.
start_date = datetime.datetime.strptime(date_last_str, '%m/%d/%Y') - datetime.timedelta(days=x)
start_date_str = datetime.datetime.strftime(start_date,'%m/%d/%Y')
print('START_DATE_STR *************************')
print(start_date_str)

##########################################################################################
### THIS IS NOT WORKING AND MAY NOT BE NECESSARY
##########################################################################################
# region_table_last_head = [['Region','Date','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative','CasesAll_Chg','C_HospYes_Res_Chg','C_HospYes_NonRes_Chg','Deaths_Chg','T_negative_Chg']]
# # Panda pull grouped by Region for the DATE_LAST_STR
# pd_last_day = data_fl[(data_fl.Date == date_last_str)][['Region','Date','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative''CasesAll_Chg','C_HospYes_Res_Chg','C_HospYes_NonRes_Chg','Deaths_Chg','T_negative_Chg']]
# region_table_last = region_table_last_head + pd_last_day.values.tolist()
# print("REGION_TABLE_LAST *******************************")
# print(region_table_last)

# Limit the universe to (A) calculate the daily changes over and then (B) run the Panda averages over
pd_xday = data_fl[(data_fl.Date > start_date_str)][['Region','Date','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']]
# pd_xday = data_fl[(data_fl.Date == '08/06/2020')][['Region','Date','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']]
region_table_means = []
print("PD_XDAY *******************************")
print(pd_xday)

# Produce a Panda pull by Region and Date and reset the index such that we can use a new dataframe with all the information
pd_region_date_sum = pd_xday.groupby(['Region','Date']).sum().reset_index()
print("PD_REGION_DATE_SUM *******************************")
print(pd_region_date_sum)

# Column headers for the sums, including the changes
region_date_sum_head = [['Region','Date','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative','CasesAll_Chg','C_HospYes_Res_Chg','C_HospYes_NonRes_Chg','Deaths_Chg','T_negative_Chg']]
region_table_means_head = [['Region','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative','CasesAll_Chg','C_HospYes_Res_Chg','C_HospYes_NonRes_Chg','Deaths_Chg','T_negative_Chg']]
region_date_sum_chg = region_date_sum_head

# Initialize the # of rows
region_date_sum_chg_row = 0

for date in reversed(date_list_lastx):
    region_date_sum_chg_row += 1
    date_last_str = date
    date_prior = datetime.datetime.strptime(date_last_str, '%m/%d/%Y') - datetime.timedelta(days=1)
    date_prior_str = datetime.datetime.strftime(date_prior, '%m/%d/%Y')
    for region in region_list:

        # Panda pull of data by region and date(x)
        day0_data = pd_region_date_sum[(pd_region_date_sum.Region == region) & (pd_region_date_sum.Date == date_last_str)][['Region','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].groupby('Region').sum()
        day0_data = day0_data.values.tolist()
        day0_data = day0_data[0]
        print(day0_data)
        day1_data = pd_region_date_sum[(pd_region_date_sum.Region == region) & (pd_region_date_sum.Date == date_prior_str)][['Region','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].groupby('Region').sum()
        day1_data = day1_data.values.tolist()
        day1_data = day1_data[0]
        print(day1_data)
        # Append a new list to the list 'region_date_chg' which consists of Region, Date, and then the differences
        region_date_sum_chg.append([region] + [date_last_str] + day0_data + list_subtract(day0_data, day1_data))
pd_region_date_sum_chg = data = pd.DataFrame(region_date_sum_chg[1:], columns=region_date_sum_chg[0])
print('PD_REGION_DATE_SUM_CHG *********************************************')
print(pd_region_date_sum_chg)

# # Create a list of lists by day with differences
# # Create the 'region_date_sum_dfc' (list of lists)
# region_date_sum_dfc = [['Region','Date','CasesAll', 'C_HospYes_Res', 'C_HospYes_NonRes', 'Deaths', 'T_negative','CasesAll_Chg', 'C_HospYes_Res_Chg', 'C_HospYes_NonRes_Chg', 'Deaths_Chg', 'T_negative_Chg']]
# for i in range(1,len(pd_region_date_sum)):
#     # USE LIST_SUBTRACT

pd_region_table_means = pd_region_date_sum_chg.groupby('Region').mean().reset_index()
print("PD_REGION_TABLE_MEANS *******************************")
print(pd_region_table_means)

# # region_table_means = []
# # region_table_means.append(pd_region_table_means.columns.tolist())
# # region_table_means = region_table_means + pd_region_table_means.values.tolist()
# # print("REGION_TABLE_MEANS *******************************")
# # print(region_table_means)

# index = pd_region_table_means.index.tolist()

# region_table_means[0].insert(0,'Region')
# for i in range(1,len(region_table_means)):
#     region_table_means[i].insert(0,index[i - 1])

region_table_means = region_table_means_head + pd_region_table_means.values.tolist()
print("REGION_TABLE_MEANS *******************************")
print(region_table_means)

# NEED TO ADD THE CHANGES TO THE TABLES IN ORDER TO DO THE REAL CALCUATIONS

# Create the 'region_table_calcs' (list of lists)
region_table_calcs = [['Region','CasesAll_Chg','C_HospYes_Calc_Chg','Deaths_Chg','Tests_Chg','Pct_Pos_Calc']]
for i in range(1,len(region_table_means)):
    # THIS IS NOT CORRECT BECAUSE IT'S ON THE TOTALS, NOT THE CHANGES. NEED TO INCORPORATE LIST_SUBTRACT FUNCTION
    cases_calc = round(region_table_means[i][6],2)
    hosp_calc = round(region_table_means[i][7] + region_table_means[i][8],2)
    deaths_calc = round(region_table_means[i][9],2)
    negatives_calc = round(region_table_means[i][10],2)
    tests_calc = cases_calc + negatives_calc
    pct_pos_calc = round((cases_calc / (cases_calc + negatives_calc) *100) , 1)
    region_table_calcs.append([region_table_means[i][0],cases_calc,hosp_calc,deaths_calc,tests_calc,pct_pos_calc])
print("REGION_TABLE_CALCS *******************************")
print(region_table_calcs)



























































































































################################################################################################################################################################
####### OLD CODE HELD HERE JUST IN CASE
################################################################################################################################################################

# rows = len(region_list)
# data_fl = pd.read_csv('covidfl.csv')
# print("data_fl *******************************")
# print(data_fl)

# # List of the dates in our CSV file
# # Recall that 'date_list_lastx' represents a list of the last X days for iteration
# print(date_list_lastx)

# # Find the last day (these will be in sequential order)
# date_last_str = date_list_lastx[-1]
# # print(date_last_str)

# # Go days back in time for the start date
# start_date = datetime.datetime.strptime(date_last_str, '%m/%d/%Y') - datetime.timedelta(days=x)
# start_date_str = datetime.datetime.strftime(start_date,'%m/%D/%Y')

# # Limit the universe to run the Panda averages over
# pd_xday = data_fl[(data_fl.Date > start_date_str)]
# region_table_means = []
# print("PD_XDAY *******************************")
# print(pd_xday)

# # This gives this output of means:
# for i in range(0,rows):
#     temp_list = []
#     # Pandas pivot table of mean of every column by Region
#     print(region_list[i])
#     region_means = pd_xday[pd_xday.Region == region_list[i]][['CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].groupby(['Region']).mean()
#     # print(region_totals)
#     temp_list.append(region_list[i])
#     temp_list = temp_list + region_means.values.tolist()[0]
#     # print(temp_list)
#     region_table_means.append(temp_list)
# print("REGION_TABLE_MEANS *******************************")
# print(region_table_means)
# #####################################################################################

# # TODO: This calculates the total hospitalizations and total tests

# # TODO: This calculates the percent positive

# ########################################################################################
# # f = open("covifl_region_date_last.txt", "w")
# # f.write(region_table_last)
# # f.close()




# ##### START HERE... I NEED TO FIGURE
# # I took this from the application.py from the finance subfolders
# @app.route("/")
# def index():
#     """Show portfolio of stocks"""
#     # Initialize the portfolio list
#     portfolio_list = []

#     # Initialize the symbol_shares list, which will be used for  the table of symbols and sum of shares.
#     symbol_shares_list = []

#     # The user_id will be used to make sure the database pull is only for the logged in user.
#     index_user_id = session["user_id"]

#     # Database pull for symbol and sum of shares, filtered where the sum of shares are greater than 0
#     symbol_shares_list = db.execute("SELECT symbol, sum(shares) FROM txns WHERE user_id = :id GROUP BY symbol HAVING sum(shares) > 0",
#             id=index_user_id)
#     stocks_in_port = len(symbol_shares_list)

#     # Set up the components that will go in the HTML table.
#     stock_value = 0.0
#     if stocks_in_port > 0:
#         for i in range(stocks_in_port):
#             # Initialize the list as list of lists with None
#             portfolio_list.append([None] * 6)
#             # Data item #1 is symbol
#             portfolio_list[i][0] = symbol_shares_list[i]["symbol"]
#             # Data item #3 is sum of the shares
#             portfolio_list[i][2] = symbol_shares_list[i]["sum(shares)"]
#             # Use IEX lookup for #2, 4, and 5
#             iex_lookup = lookup(symbol_shares_list[i]["symbol"])
#             # Data item #2 is name of the stock
#             portfolio_list[i][1] = iex_lookup["name"]
#             # Data item #4 is name of the stock
#             portfolio_list[i][3] = usd(iex_lookup["price"])
#             # Data item #5 is the current value of the stock (price x current total shares)
#             portfolio_list[i][4] = iex_lookup["price"] * symbol_shares_list[i]["sum(shares)"]
#             # Data item #6 is the string representation of Data item #5 (current stock value)
#             portfolio_list[i][5] = usd(portfolio_list[i][4])
#             # This updates the total stock value with Data item #5 (current stock value)
#             stock_value = stock_value + float(portfolio_list[i][4])
#         # print(portfolio_list)
#         # print("Stocks total = " + usd(stock_value))

#     # Database pull in order to get the cash from the logged in user
#     rows = db.execute("SELECT cash FROM users WHERE id = :id",
#               id=index_user_id)
#     cash = rows[0]["cash"]
#     # print("Cash total = " + usd(cash))
#     port_value = stock_value + cash
#     # print("Grand total = " + usd(port_value))
#     # Get the number of rows in the portfolio, which will be used in the index table
#     rows = len(portfolio_list)
#     # print("rows for portfolio = " + str(rows))
#     return render_template("index.html", portfolio_list=portfolio_list, stock_value=usd(stock_value), cash=usd(cash), port_value=usd(port_value), rows=rows)