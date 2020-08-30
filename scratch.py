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

# Configure application
app = Flask(__name__)

# # Ensure templates are auto-reloaded
# app.config["TEMPLATES_AUTO_RELOAD"] = True

# # Ensure responses aren't cached
# @app.after_request
# def after_request(response):
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response

# Custom filter
# app.jinja_env.filters["usd"] = usd

# # Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_FILE_DIR"] = mkdtemp()
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

test = [['ABC',1,2,3,4,5],['DEF',6,7,8,9,10]]

# I took this from the application.py from the finance subfolders
@app.route("/")
def index():
    test.append(['GHI',11,12,13,14,15])
    print(test)

    # print("Grand total = " + usd(port_value))
    # Get the number of rows in the portfolio, which will be used in the index table
    rows = len(test)
    # print("rows for portfolio = " + str(rows))
    return render_template("index.html", test=test, rows=rows)

# # ex = list()
# print(ex)
# ex.append(1)
# print(ex)
# ex.append(2)
# print(ex)

# This is the temp DictReader using the sample CSV
# cr = csv.DictReader(open("flcv19test.csv", "r"))
# with open(cr, 'w', newline='') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=cr.fieldnames())

# for row in cr:
#     print(row)

# response = requests.get("https://jsonplaceholder.typicode.com/todos")
# todos = json.loads(response.text)
# print(type(todos))
# for row in todos:
#     print(row)

# Testing how to append dicts
# list_dict_1 = [{'attributes': {'County': 'Broward', 'Age': '56', 'Age_group': '55-64 years', 'EDvisit': 'UNKNOWN', 'Hospitalized': 'UNKNOWN', 'Died': 'NA', 'EventDate': 1595367610000, 'ObjectId': 2000}}, {'attributes': {'County': 'Orange', 'Age': '54', 'Age_group': '45-54 years', 'EDvisit': 'NO', 'Hospitalized': 'NO', 'Died': 'NA', 'EventDate': 1594598400000, 'ObjectId': 1997}}]
# list_dict_2 = [{'attributes': {'County': 'Holmes', 'Age': '35', 'Age_group': '35-44 years', 'EDvisit': 'NO', 'Hospitalized': 'NO', 'Died': 'NA', 'EventDate': 1594598400000, 'ObjectId': 1992}}, {'attributes': {'County': 'Bay', 'Age': '44', 'Age_group': '35-44 years', 'EDvisit': 'UNKNOWN', 'Hospitalized': 'UNKNOWN', 'Died': 'NA', 'EventDate': 1595367018000, 'ObjectId': 1993}}]
# print(len(list_dict_1))
# for x in list_dict_1:
#     print("******************")
#     print(x)
# for i in range(len(list_dict_2)):
#     list_dict_1.append(list_dict_2[i])
# print("*******************************************")
# print(list_dict_1)
# print(list_dict_1[-1]['attributes']['ObjectId'])

# Testing how to find something in a string
# string = "asd;fkljqwerpioyvvlakjdhqlkrjhqwerhyalvhjsljhsdhttps://www.arcgis.com/sharing/rest/content/items/674788c8426740febef37704242b9ec8/datawerptiuofkl;sjf;klqjwrtopiurtas"
# before, sep, after = string.partition("https://www.arcgis.com/sharing/rest/content/items/")
# before, sep, after = after.partition("/data")
# print(before)

# ##########################################################################################################
# # Testing out getting the string for the USF URL
# yr = 2020
# mo = 7
# dy = 25

# # TODO: SET UP A LOOP TO GET THE DAILY CSV DATA
# def date_set(month, day, year):
#     # This runs through the dates
#     mo_str = "0" + str(month)
#     if dy < 10:
#         dy_str = "0" + str(day)
#     else:
#         dy_str = str(dy)

#     yr_str = str(yr)
#     date_str = mo_str + dy_str + yr_str
#     return(date_str)
#     # for mo in range(6,8):
#     #     mo_str = "0" + str(mo)

# date_str = date_set(mo, dy, yr)
# print(date_str)

# date1 = datetime.datetime(yr, mo, dy).strftime("%x")
# # date1_f =
# print("Date1 = ", date1)

# date2 = datetime.datetime(yr, mo, dy + 3).strftime("%x")
# print("Date2 = ", date2)

# date_dfc = datetime.datetime.strptime(date2, "%x").toordinal()- datetime.datetime.strptime(date1, "%x").toordinal()
# print(date_dfc)

# print(type(date1))

# # Function to convert the dates to a number for computation
# def date_ordinal(date):
#     # date has to be a string
#     date_ord = datetime.datetime.strptime(date, "%x").toordinal()
#     return(date_ord)

# print(date_ordinal(date2) - date_ordinal(date1))

##########################################################################################################
# with open('covidfl.csv', mode='r') as covidfl:
#     test = csv.reader(covidfl, delimiter=',')
#     covidfl_list = list(test)
# print(covidfl_list)

########################################################################################
# csv_rows = 2
# csv_data = [['1','2','3'],['4','5','6']]
# date_f = '07/25/2020'
# for i in range(0,csv_rows):
#     csv_data[i].append(date_f)

#     with open('covidfl.csv', mode='a') as covidfl:
#         writer = csv.writer(covidfl, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
#         writer.writerow(csv_data[i])

######################################################################################

# startDate = '06012020'

# start = datetime.datetime.strptime(startDate, '%m%d%Y')
# print(type(start))
# end = datetime.datetime.today() - datetime.timedelta(days=1)
# print(end)
# print(type(end))
# days_iter = end.toordinal() - start.toordinal()
# print(type(days_iter))

# # Iterate over the days
# for dayNum in range(0, days_iter + 1):
#     date = start + datetime.timedelta(days=dayNum)
#     date_str = datetime.datetime.strftime(date, '%m%d%Y')
#     print(date_str)
#     date_f = date.strftime('%m/%d/%Y')
#     print(date_f)

################################################################################

# import os, datetime, time, json, csv, statistics, zipfile
# from pathlib import Path
# import requests
# import urllib.request
# import pandas as pd
# from io import BytesIO
# from urllib.request import urlopen
# from zipfile import ZipFile

# startDate = '06222020'

# start = datetime.datetime.strptime(startDate, '%m%d%Y')
# print(type(start))
# end = datetime.datetime.today() - datetime.timedelta(days=1)
# print(end)
# print(type(end))
# days_iter = end.toordinal() - start.toordinal()
# print(type(days_iter))

# # Iterate over the days
# for dayNum in range(0, days_iter + 1):
#     date = start + datetime.timedelta(days=dayNum)
#     date_str = datetime.datetime.strftime(date, '%m%d%Y')
#     # print(date_str)
#     date_f = date.strftime('%m/%d/%Y')
#     # print(date_f)
#     if date_f == '07/04/2020':
#         continue

#     # From USF archive of DOH data. These compile stats from CSV. Each file is about 70 rows.
#     url_step1 = "https://covid19-usflibrary.hub.arcgis.com/datasets/florida-covid19-" + date_str + "-bycounty-csv"
#     url = url_step1

#     # Extract the long string from the website that identifies the file name.
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#     except:
#         print("Download problem on " + date_f)
#     # print(response.text)
#     http_code = response.text
#     before, sep, after = http_code.partition("https://www.arcgis.com/sharing/rest/content/items/")
#     before, sep, after = after.partition("/info")
#     csv_loc = before
#     # print(before)

#     # Get the URL of the CSV data by concatenation
#     url = "https://www.arcgis.com/sharing/rest/content/items/" + csv_loc + "/data"

#     # response = requests.get(url)
#     # response.raise_for_status()
#     # print(type(response))
#     # cr = csv.reader(response, delimiter=',')
#     # print(type(cr))

#     # Open the URL, unzip the file, and read in the CSV
#     try:
#         resp = urlopen(url)
#         zipped = ZipFile(BytesIO(resp.read()))
#         csv_file = open(zipped.extract('Florida_COVID_Cases_0.csv'))
#     except:
#         print("Unzip problem on " + date_f)
#     csv_read = csv.reader(csv_file)
#     csv_data = list(csv_read)
#     # Count the rows in the file
#     csv_rows = len(csv_data)
#     csv_cols = len(csv_data[1])
#     # print(csv_data[0][83])
#     if csv_data[0][82] != 'Deaths':
#         print('Date = ' + date_str)
#         print('column 82 = ' + csv_data[0][82])
#         print(csv_data[0].index('Deaths'))

# Gets today's date and the previous date
# date_last_str = '07/30/2020'
# date_prior = datetime.datetime.strptime(date_last_str, '%m/%d/%Y') - datetime.timedelta(days=1)
# date_prior_str = datetime.datetime.strftime(date_prior, '%m/%d/%Y')
# print(date_prior_str)

# # Run through quick example of combining lists
# a = [1, 2, 3, 4]
# b = [4, 3, 2, 1]
# c = [1, 1, 1, 1]
# d = [a] + [b]
# print(d)
# print(d[1][2])

# region = 'Region'
# date_last_str = '8/9/2020'
# day0_data = 50
# temp_subtract = 5
# region_date_chg = [['Region','Date','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative','CasesAll_Chg','C_HospYes_Res_Chg','C_HospYes_NonRes_Chg','Deaths_Chg','T_negative_Chg']]
# region_date_chg.append([region] + [date_last_str] + day0_data + temp_subtract)
# print(region_date_chg)

# def list_subtract(list1, list2):
#     list_dfc = []
#     list1_len = len(list1)
#     list2_len = len(list2)
#     for i in range(list1_len):
#         list_dfc.append(list1[i] - list2[i])
#     return(list_dfc)

# c = list_subtract(a, b)
# print(type(a))
# print(type(c))
# print(c)
# d = a + c
# print(d)

# Function to add the items in the list to one another (adding two lists - used for Tampa region)
# def list_add2(list1, list2):
#     list_add = []
#     list1_len = len(list1)
#     list2_len = len(list2)
#     if list1_len != list2_len:
#         print("Lists must have the same number of items")
#     for i in range(list1_len):
#         list_add.append(list1[i] + list2[i])
#     return(list_add)

# # Function to add the items in the list to one another (adding two lists - used for Tampa region)
# def list_add3(list1, list2, list3):
#     list_add = []
#     list1_len = len(list1)
#     list2_len = len(list2)
#     list3_len = len(list3)
#     if list1_len != list2_len:
#         print("Lists must have the same number of items")
#     if list1_len != list3_len:
#         print("Lists must have the same number of items")
#     for i in range(list1_len):
#         list_add.append(list1[i] + list2[i] + list3[i])
#     return(list_add)

# print(list_add3(a,b,c))
# print(list_add2(b,c))

# # **************** This is not currently working in full, but it's good to have all the parameters in place for now.
# date_list = ['07/20/2020', '07/21/2020', '07/22/2020', '07/23/2020', '07/24/2020', '07/25/2020', '07/26/2020', '07/27/2020', '07/28/2020', '07/29/2020', '07/30/2020', '07/31/2020', '08/01/2020']
# county_list = ['Gilchrist', 'Putnam', 'Taylor', 'Okaloosa', 'Calhoun', 'Palm Beach', 'St. Lucie', 'Pasco', 'Gadsden', 'Leon', 'Jefferson', 'Madison', 'Liberty', 'Hamilton', 'Bay', 'Columbia', 'Baker', 'Holmes', 'Martin', 'Hillsborough', 'Manatee', 'Clay', 'Hardee', 'Marion', 'Volusia', 'Dixie', 'Lake', 'Levy', 'Sumter', 'Seminole', 'Orange', 'Citrus', 'Hernando', 'Pinellas', 'Suwannee', 'Duval', 'Lafayette', 'Gulf', 'Union', 'Bradford', 'Wakulla', 'Brevard', 'Polk', 'Osceola', 'Highlands', 'Lee', 'Collier', 'Dade', 'Monroe', 'Santa Rosa', 'Walton', 'Jackson', 'Washington', 'Nassau', 'Glades', 'Charlotte', 'Sarasota', 'Desoto', 'Flagler', 'Hendry', 'Indian River', 'Broward', 'Escambia', 'Okeechobee', 'Franklin', 'Alachua', 'St. Johns', 'Unknown', 'State']
# region_list = ['Collier', 'Lee', ['Dade','Broward','Palm Beach'],['Hillsborough','Pinellas'],['Orange','Polk','Osceola'],['Duval','St. Johns'],'State']
# print(date_list[-3:])
# for date in reversed(date_list):
#     for i in range(0,7):
#         if region_list[i]
#             if type(region) == list:
#                 for county_region in region:
#                     print(county_region + county + date)

###############################################

# region_date_chg = [['Region', 'Date', 'CasesAll', 'C_HospYes_Res', 'C_HospYes_NonRes', 'Deaths', 'T_negative', 'CasesAll_Chg', 'C_HospYes_Res_Chg', 'C_HospYes_NonRes_Chg', 'Deaths_Chg', 'T_negative_Chg'], ['Collier', '08/03/2020', 9811, 675, 12, 124, 50047, 77, 3, 0, 0, 447], ['Lee', '08/03/2020', 15799, 996, 17, 300, 94046, 125, 5, 0, 0, 508], ['South Florida', '08/03/2020', 34550, 2602, 27, 845, 229991, 324, 8, 0, 12, 1683], ['Tampa Bay Region', '08/03/2020', 30450, 1290, 12, 348, 197854, 332, 8, 0, 1, 2502], ['Orlando Region', '08/03/2020', 29927, 856, 41, 239, 228753, 228, 8, 0, 5, 1600], ['Jacksonville Region', '08/03/2020', 21830, 626, 15, 160, 177655, 165, 1, 0, 2, 1125], ['Rest of Florida', '08/03/2020', 331, 19, 0, 3, 3126, -3, 0, 0, 0, 20], ['State', '08/03/2020', 491884, 27366, 378, 7157, 3260914, 4752, 216, 4, 73, 27049], ['Collier', '08/02/2020', 9734, 672, 12, 124, 49600, 72, 4, 0, 0, 337], ['Lee', '08/02/2020', 15674, 991, 17, 300, 93538, 123, 10, 0, 0, 447], ['South Florida', '08/02/2020', 34226, 2594, 27, 833, 228308, 372, 9, 0, 0, 1951], ['Tampa Bay Region', '08/02/2020', 30118, 1282, 12, 347, 195352, 529, 9, 0, 6, 2872], ['Orlando Region', '08/02/2020', 29699, 848, 41, 234, 227153, 233, 9, 0, 2, 1717], ['Jacksonville Region', '08/02/2020', 21665, 625, 15, 158, 176530, 343, 0, 0, 1, 2389], ['Rest of Florida', '08/02/2020', 334, 19, 0, 3, 3106, 5, 0, 0, 0, 26], ['State', '08/02/2020', 487132, 27150, 374, 7084, 3233865, 7104, 178, 2, 62, 34450]]
# print(region_date_chg[1][1])

#############################################
# # 8/11/2020
# # Panda pull of fake CSV data and limits by date and then sums totals
# regions = ['Miami','Tampa','Orlando']
# rows = len(regions)
# pd_raw = pd.read_csv('Region_Date_Temp.csv')
# # print(pd_raw)

# # Instead of hardcoding the date, I will need to use the datetime function
# # List of the dates in our CSV file
# date_list_lastx = ['7/29/2020','7/30/2020','7/31/2020','8/1/2020','8/2/2020','8/3/2020']

# # How many days to do the average over
# days = 5

# # Find the last day (these will be in sequential order)
# date_last_str = date_list_lastx[-1]
# # print(date_last_str)

# # Go days back in time for the start date
# start_date = datetime.datetime.strptime(date_last_str, '%m/%d/%Y') - datetime.timedelta(days=days)
# start_date_str = datetime.datetime.strftime(start_date,'%-m/%-e/%Y')

# # Limit the universe to run the Panda averages over
# pd_3day = pd_raw[(pd_raw.Date > start_date_str)]
# new_list = []

# # This gives this output of means:
# for i in range(0,rows):
#     temp_list = []
#     # Pandas pivot table of mean of every column by Region
#     region_totals = pd_3day[pd_3day.Region == regions[i]].groupby(['Region']).mean()
#     # print(region_totals)
#     temp_list.append(regions[i])
#     temp_list = temp_list + region_totals.values.tolist()[0]
#     # print(temp_list)
#     new_list.append(temp_list)
# print(new_list)

# *******************************************
# 8/11/2020
# This gets the last date and establishes the dates to calculate over
# date_list_lastx = ['7/29/2020','7/30/2020','7/31/2020']
# days = 4
# date_last_str = date_list_lastx[-1]
# print(date_last_str)
# next_date = datetime.datetime.strptime(date_last_str, '%m/%d/%Y') - datetime.timedelta(days=days)
# print(datetime.datetime.strftime(next_date,'%m/%d/%Y'))

########################################################
# This segment are things that are already in the COVID_USF.PY file.
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

region_list = ['Collier','Lee','South Florida','Tampa Bay Region','Orlando Region','Jacksonville Region','Rest of Florida','State']
date_list_lastx = ['08/03/2020','08/04/2020','08/05/2020','08/06/2020']
x = 4

# Panda pull of fake CSV data and limits by date and then sums totals
# Recall that 'region_list' is our list of regions for iteration

rows = len(region_list)
pd_raw = pd.read_csv('covidfl.csv',delimiter=',', quotechar="'")

# List of the dates in our CSV file
# Recall that 'date_list_lastx' represents a list of the last X days for iteration

last_date_panda = pd_raw.Date.max()
print('LAST_DATE_PANDA *************************')
print(last_date_panda)
print('DATE_LIST_LASTX *************************')
print(date_list_lastx)

# Find the last day (these will be in sequential order)
date_last_str = date_list_lastx[-1]
print('DATE_LAST_STR *************************')
print(date_last_str)

# Go X days back in time for the start date. It's (x+1) because we need an extra day back to calculate the differences
start_date = datetime.datetime.strptime(date_last_str, '%m/%d/%Y') - datetime.timedelta(days=x+1)
start_date_str = datetime.datetime.strftime(start_date,'%m/%d/%Y')
print('START_DATE_STR *************************')
print(start_date_str)

# Limit the universe to (A) calculate the daily changes over and then (B) run the Panda averages over
pd_xday = pd_raw[(pd_raw.Date > start_date_str)][['Region','Date','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']]
# pd_xday = pd_raw[(pd_raw.Date == '08/06/2020')][['Region','Date','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']]
region_table_means = []
print("PD_XDAY *******************************")
print(pd_xday)

pd_region_date_sum = pd_xday.groupby(['Region','Date']).sum().reset_index()
print("PD_REGION_DATE_SUM *******************************")
print(pd_region_date_sum)

# # Print the list
# print("REGION_DATE_SUM (list of lists)*******************************")
# print(region_date_sum)

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
        day0_data = pd_region_date_sum[(pd_region_date_sum.Region == region) & (pd_region_date_sum.Date == date_last_str)][['CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].values.tolist()
        # day0_data = pd_region_date_sum[(pd_region_date_sum.Date == date_last_str)][['CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].values.tolist()
        day0_data = day0_data[0]
        # Panda pull of data by region and date(x -1)
        # day1_data = pd_region_date_sum[(pd_region_date_sum.Date == date_prior_str)][['CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].values.tolist()
        day1_data = pd_region_date_sum[(pd_region_date_sum.Region == region) & (pd_region_date_sum.Date == date_prior_str)][['CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].values.tolist()
        day1_data = day1_data[0]
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


# This gives this output of means:
# for i in range(0,rows):
#     temp_list = []
#     print(region_list[i])
#     # Pandas pivot table to get the totals in the relevant columns by Region and By Day. This is an interim step.
#     region_means = pd_region_date_sum.head(3)
#     # pd_region_date_sum = pd_xday[pd_xday.Region == region_list[i]][['CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].groupby(['Region'])

#     print(region_means)
#     temp_list.append(region_list[i])
#     temp_list = temp_list + region_means.values.tolist()[0]
#     # print(temp_list)
#     region_table_means.append(temp_list)
# print("REGION_TABLE_MEANS *******************************")
# print(region_table_means)