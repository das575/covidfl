import os, datetime, time, csv, statistics
# from pathlib import Path
import requests
import urllib.request
import pandas as pd
# import numpy as np
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
# The following import is from my own custom function file.
from covidfl_helpers import list_subtract, list_add2, list_add3, commas_place, pct

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def covidfl():
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

    print(region('Gilchrist'))

    date_max_csv = data_fl['Date'].max()
    # print('\nDATE_MAX_CSV: ',date_max_csv)

    # Initialize the date list
    date_list = list(data_fl['Date'].unique())
    # print('\nDATE_LIST: ',date_list)

    start = datetime.datetime.strptime(date_max_csv, '%m/%d/%Y') + datetime.timedelta(days=1)
    # print('\nSTART: ',start)

    # If the CSV file is already updated to today, then skip all the dating information.
    if datetime.datetime.strptime(date_max_csv, '%m/%d/%Y').date() != datetime.date.today():
        #################
        # if dating information is required, then first test for 404
        today = datetime.datetime.strftime(datetime.date.today(), '%m%d%Y')
        print('\nTODAY **************************************** ', today)
        url = "https://covid19-usflibrary.hub.arcgis.com/datasets/florida-covid19-" + today + "-bycounty-csv"
        try:
            response = requests.get(url)
            response.raise_for_status()
        except:
            print("Download problem on " + date_f)
        http_code = response.text

        # Checks to make sure that the URL gives us data, not a 404. If it's good, we will proceed with parsing the file and reading and writing the csv
        if 'content="https://covid19-usflibrary.hub.arcgis.com/404' not in http_code[0:2000]:
            end = datetime.date.today()
        else:
            end = datetime.date.today() - datetime.timedelta(days=1)
        print('END ********************************\n', end)
        # Sets the days to iterate for the file getting loop
        days_iter = end.toordinal() - start.toordinal()
    else:
        days_iter = 0

    # Initialize the data_is_late indicator to 0. It will be 1 if the latest data isn't available.
    data_is_late = 0

    # Iterate over the days from start to end: gets the CSV for each day
    for dayNum in range(0, days_iter + 1):
        date = start + datetime.timedelta(days=dayNum)
        date_str = datetime.datetime.strftime(date, '%m%d%Y')
        # print('\nDATE_STR: ',date_str)
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

        # Checks to make sure that the URL gives us data, not a 404. If it's good, we will proceed with parsing the file and reading and writing the csv
        if 'content="https://covid19-usflibrary.hub.arcgis.com/404' not in http_code[0:2000]:
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

            # Append each row with date_f
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
        else:
            date_list.remove(date_f)
            data_is_late = 1

    # print(counties)
    # Limit the date list to the final X number of days for iteration
    date_count = len(date_list)
    x = 7

    if x > date_count:
        print("Increase the number of downloaded days")
    else:
        date_list_lastx = date_list[-x:]

    # print('\nDATE_LIST: ',date_list)
    # print('\nDATE_LIST_LASTX: ',date_list_lastx)

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
        # print('\nDATE_LAST_STR: ',date_last_str)
        # print('\nDATE_PRIOR_STR: ',date_prior_str)
        for region in region_list:

            # Panda pull of data by region and date(x)
            day0_data = data_fl[(data_fl.Region == region) & (data_fl.Date == date_last_str)][['Region','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].groupby('Region').sum()
            day0_data = day0_data.values.tolist()
            # if region_date_chg_row == 1:
                # print('\nREGION: ',region)
                # print('DATE_LAST_STR: ',date_last_str)
                # print('DAY0_DATA: ',day0_data)
            day0_data = day0_data[0]
            # print(day0_data)
            # Panda pull of data by region and date(x -1)
            day1_data = data_fl[(data_fl.Region == region) & (data_fl.Date == date_prior_str)][['Region','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].groupby('Region').sum()
            day1_data = day1_data.values.tolist()
            day1_data = day1_data[0]
            # Append a new list to the list 'region_date_chg' which consists of Region, Date, and then the differences
            # print('\nREGION: ',region)
            # print('DATE_LAST_STR: ',date_last_str)
            # print('DAY0_DATA: ',day0_data)
            # print('DAY1_DATA: ',day1_data)
            # print('DIFFERENCE: ',list_subtract(day0_data, day1_data))
            region_date_chg.append([region] + [date_last_str] + day0_data + list_subtract(day0_data, day1_data))
    # print('REGION_DATE_CHG *********************************************')
    # print(region_date_chg)
    # print('Number of rows in region_date_chg: ' + str(len(region_date_chg)))
    region_table_last = region_date_chg[0:9]
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
    # print('LAST_DATE_PANDA *************************')
    # print(last_date_panda)
    # print('DATE_LIST_LASTX *************************')
    # print(date_list_lastx)

    # Find the last day (these will be in sequential order)
    date_last_str = date_list_lastx[-1]
    # print('DATE_LAST_STR *************************')
    # print(date_last_str)

    # Go X days back in time for the start date.
    start_date = datetime.datetime.strptime(date_last_str, '%m/%d/%Y') - datetime.timedelta(days=x+1)
    start_date_str = datetime.datetime.strftime(start_date,'%m/%d/%Y')
    # print('START_DATE_STR *************************')
    # print(start_date_str)

    # Limit the universe to (A) calculate the daily changes over and then (B) run the Panda averages over
    pd_xday = data_fl[(data_fl.Date > start_date_str)][['Region','Date','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']]
    # pd_xday = data_fl[(data_fl.Date == '08/06/2020')][['Region','Date','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']]
    region_table_means = []
    # print("PD_XDAY *******************************")
    # print(pd_xday)

    # Produce a Panda pull by Region and Date and reset the index such that we can use a new dataframe with all the information
    pd_region_date_sum = pd_xday.groupby(['Region','Date']).sum().reset_index()
    # print("PD_REGION_DATE_SUM *******************************")
    # print(pd_region_date_sum)

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
            day1_data = pd_region_date_sum[(pd_region_date_sum.Region == region) & (pd_region_date_sum.Date == date_prior_str)][['Region','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].groupby('Region').sum()
            day1_data = day1_data.values.tolist()
            day1_data = day1_data[0]
            # print(region,date_last_str,date_prior_str,day0_data, day1_data)
            # Append a new list to the list 'region_date_chg' which consists of Region, Date, and then the differences
            region_date_sum_chg.append([region] + [date_last_str] + day0_data + list_subtract(day0_data, day1_data))
    pd_region_date_sum_chg = data = pd.DataFrame(region_date_sum_chg[1:], columns=region_date_sum_chg[0])
    # print('PD_REGION_DATE_SUM_CHG *********************************************')
    # print(pd_region_date_sum_chg)

    # # Create a list of lists by day with differences
    # # Create the 'region_date_sum_dfc' (list of lists)
    # region_date_sum_dfc = [['Region','Date','CasesAll', 'C_HospYes_Res', 'C_HospYes_NonRes', 'Deaths', 'T_negative','CasesAll_Chg', 'C_HospYes_Res_Chg', 'C_HospYes_NonRes_Chg', 'Deaths_Chg', 'T_negative_Chg']]
    # for i in range(1,len(pd_region_date_sum)):
    #     # USE LIST_SUBTRACT

    pd_region_table_means = pd_region_date_sum_chg.groupby('Region').mean().reset_index()
    # print("PD_REGION_TABLE_MEANS *******************************")
    # print(pd_region_table_means)

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

    # Re-sorts the means table so it matches the region_last_calcs:
    region_table_means_temp = [region_table_means[0]]
    for region in region_list:
        for i in range(1,len(region_table_means)):
            if region_table_means[i][0] == region:
                region_table_means_temp.append(region_table_means[i])
    region_table_means = region_table_means_temp
    print("REGION_TABLE_MEANS *******************************")
    print(region_table_means)


    # Create the 'region_last_calcs' (list of lists)
    region_last_calcs = [['Region','CasesAll_Chg','C_HospYes_Calc_Chg','Deaths_Chg','Tests_Chg','Pct_Pos_Calc']]
    for i in range(1,len(region_table_last)):
        # This all have a '+1' because there's an extra column in this table because of the Date
        cases_calc = round(region_table_last[i][6+1],0)
        hosp_calc = round(region_table_last[i][7+1] + region_table_last[i][8+1],0)
        deaths_calc = round(region_table_last[i][9+1],0)
        negatives_calc = round(region_table_last[i][10+1],0)
        tests_calc = round(cases_calc + negatives_calc,0)
        pct_pos_calc = round((cases_calc / (cases_calc + negatives_calc) *100) , 1)
        region_last_calcs.append([region_table_last[i][0],commas_place(cases_calc),commas_place(hosp_calc),commas_place(deaths_calc),commas_place(tests_calc),pct(pct_pos_calc)])
    print("REGION_LAST_CALCS *******************************")
    print(region_last_calcs)

    # Create the 'region_table_calcs' (list of lists)
    region_table_calcs = [['Region','CasesAll_Chg','C_HospYes_Calc_Chg','Deaths_Chg','Tests_Chg','Pct_Pos_Calc']]
    for i in range(1,len(region_table_means)):
        cases_calc = round(region_table_means[i][6],1)
        hosp_calc = round(region_table_means[i][7] + region_table_means[i][8],1)
        deaths_calc = round(region_table_means[i][9],1)
        negatives_calc = round(region_table_means[i][10],1)
        tests_calc = round(cases_calc + negatives_calc,1)
        pct_pos_calc = round(cases_calc / (cases_calc + negatives_calc) * 100, 1)
        region_table_calcs.append([region_table_means[i][0],commas_place(cases_calc),commas_place(hosp_calc),commas_place(deaths_calc),commas_place(tests_calc),pct(pct_pos_calc)])
    print("REGION_TABLE_CALCS *******************************")
    print(region_table_calcs)

    final_table = [region_last_calcs,region_table_calcs,date_max,data_is_late]
    print("FINAL_TABLE *******************************")
    print(final_table)
    return(final_table)

# Undo this if you need to run the program in covidfl in the Terminal on its own.
# covidfl()
