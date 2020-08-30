# importing pandas as pd
import pandas as pd
import datetime, csv
from urllib.request import urlopen
import mimetypes, requests

# # Create the dataframe
# df = pd.DataFrame({'Date':['10/2/2011', '11/2/2011', '12/2/2011', '13/2/11'],
#                     'Event':['Music', 'Poetry', 'Theatre', 'Comedy'],
#                     'Cost':[10000, 5000, 15000, 2000]})

# # Print the dataframe
# print(df)

# # Create an empty list
# Row_list =[]

# # Iterate over each row
# for i in range((df.shape[0])):

#     # Using iloc to access the values of
#     # the current row denoted by "i"
#     Row_list.append(list(df.iloc[i, :]))

# # Print the list
# print(Row_list)
######################################

# try:
#     data_fl = pd.read_csv('covidfl.csv', delimiter=',', quotechar="'",  header=0)
# except:
#     print('covidfl.csv file does not exist')

# print(data_fl[(data_fl.Region == 'State') & (data_fl.Date == '08/09/2020')][['Region','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].values.tolist())


# date_max_csv = data_fl['Date'].max()
# print(date_max_csv)

# start = datetime.datetime.strptime(date_max_csv, '%m/%d/%Y') + datetime.timedelta(days=1)
# print(start)
# print(datetime.datetime.strptime(date_max_csv, '%m/%d/%Y').date() != datetime.datetime.today())
# print(datetime.date.today())
# print(datetime.datetime.strptime(date_max_csv, '%m/%d/%Y').date())

# date_list = list(data_fl['Date'].unique())
# print(date_list)
# print('\nDATE_LIST:',date_list)

###########################################

# url = 'https://www.arcgis.com/sharing/rest/content/items/8f40b188b54b47d09347926002ca7fd9/data'
# resp = urlopen(url)

# try:
#     resp = urlopen(url)
#     zipped = ZipFile(BytesIO(resp.read()))
#     csv_file = open(zipped.extract('Florida_COVID_Cases_0.csv'))
# except:
#     csv_down = requests.get(url)
#     csv_down.raise_for_status()
#     csv_file = open('Florida_COVID_Cases_0.csv')
# else:
#     print("Unzip problem on " + date_f)
# csv_read = csv.reader(csv_file)
# csv_data_raw = list(csv_read)
# print(len(csv_data_raw))

#################################

# def region(county):
#     if county == 'Collier':
#         region = 'Collier'
#     elif county == 'Lee':
#         region = 'Lee'
#     elif county == 'Dade' or county == 'Broward' or county == 'Palm Beach':
#         region = 'South Florida'
#     elif county == 'Hillsborough' or county == 'Pinellas':
#         region = 'Tampa Bay Region'
#     elif county == 'Orange' or county == 'Polk' or county == 'Osceola':
#         region = 'Orlando Region'
#     elif county == 'Duval' or county == 'St. Johns':
#         region = 'Jacksonville Region'
#     elif county == 'State':
#         region = 'State'
#     else:
#         region = 'Rest of Florida'
#     return(region)

# county = input('County? ')
# region = region(county)
# print(region)

#########################################33

# a = [[2]]
# print(a[0])

# region = 'South Florida'
# date_last_str = '08/18/2020'
# date_prior_str = '08/17/2020'
# try:
#     pd_region_date_sum = pd.read_csv('covidfl.csv', delimiter=',', quotechar="'",  header=0)
# except:
#     print('covidfl.csv file does not exist')

# day0_data = data_fl[(data_fl.Region == region) & (data_fl.Date == date_last_str)][['Region','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].groupby('Region').sum()
# day0_data = day0_data.values.tolist()
# print(day0_data)
# print(type(day0_data))
# print(day0_data[0])
# day0_data = pd_region_date_sum[(pd_region_date_sum.Region == region) & (pd_region_date_sum.Date == date_last_str)][['Region','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].groupby('Region').sum()
# day0_data = day0_data.values.tolist()
# day0_data = day0_data[0]
# print(day0_data)
# day1_data = pd_region_date_sum[(pd_region_date_sum.Region == region) & (pd_region_date_sum.Date == date_prior_str)][['Region','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].groupby('Region').sum()
# day1_data = day1_data.values.tolist()
# day1_data = day1_data[0]
# print(day1_data)

########################################

# # Function to subtract the items in the list from one another. This is used to calculate the daily changes
# def list_subtract(list1, list2):
#     list_dfc = []
#     list1_len = len(list1)
#     list2_len = len(list2)
#     if list1_len != list2_len:
#         print("Lists must have the same number of items")
#     for i in range(list1_len):
#         list_dfc.append(list1[i] - list2[i])
#     return(list_dfc)

# a = [5,5,5,5]
# b = [1,1,1,1]
# print(list_subtract(a,b))

# #############################################
# region_list = ['Collier','Lee','South Florida','Tampa Bay Region','Orlando Region','Jacksonville Region','Rest of Florida','State']
# region_table_means = [['Region', 'CasesAll', 'C_HospYes_Res', 'C_HospYes_NonRes', 'Deaths', 'T_negative', 'CasesAll_Chg', 'C_HospYes_Res_Chg', 'C_HospYes_NonRes_Chg', 'Deaths_Chg', 'T_negative_Chg'], ['Collier', 10924.42857142857, 774.7142857142857, 15.0, 155.42857142857142, 54846.42857142857, 65.0, 6.285714285714286, 0.14285714285714285, 1.8571428571428572, 326.0], ['Jacksonville Region', 28713.85714285714, 1003.2857142857143, 22.0, 271.7142857142857, 235447.57142857142, 173.28571428571428, 13.0, 0.0, 4.0, 1327.142857142857], ['Lee', 17450.85714285714, 1212.857142857143, 19.428571428571427, 379.57142857142856, 102925.71428571429, 98.71428571428571, 17.857142857142858, 0.2857142857142857, 3.5714285714285716, 867.0], ['Orlando Region', 59398.142857142855, 3199.0, 62.857142857142854, 841.1428571428571, 399306.5714285714, 424.14285714285717, 39.142857142857146, -0.14285714285714285, 14.142857142857142, 2718.714285714286], ['Rest of Florida', 154596.42857142858, 10455.285714285714, 122.57142857142857, 2814.8571428571427, 1245535.4285714286, 1509.0, 158.71428571428572, 0.8571428571428571, 51.57142857142857, 8338.0], ['South Florida', 252140.42857142858, 14323.42857142857, 137.42857142857142, 4092.714285714286, 1253449.2857142857, 1883.2857142857142, 173.0, 0.14285714285714285, 67.71428571428571, 10040.285714285714], ['State', 576430.4285714285, 34354.71428571428, 415.57142857142856, 9602.285714285714, 3676401.714285714, 4495.0, 444.7142857142857, 1.4285714285714286, 162.28571428571428, 26024.14285714286], ['Tampa Bay Region', 53206.28571428572, 3386.1428571428573, 36.285714285714285, 1046.857142857143, 384890.71428571426, 341.57142857142856, 36.714285714285715, 0.14285714285714285, 19.428571428571427, 2407.0]]
# print('REGION_TABLE_MEANS (ORIGINAL): ',region_table_means)
# # Re-sorts the means table so it matches the region_last_calcs:
# print('\nREGION_TABLE_MEANS[2][6] (TYPE): ',type(region_table_means[2][6]))
# print(round(region_table_means[2][6],2))
# region_table_means_temp = [region_table_means[0]]
# for region in region_list:
#     for i in range(1,len(region_table_means)):
#         if region_table_means[i][0] == region:
#             region_table_means_temp.append(region_table_means[i])
# print("REGION_TABLE_MEANS_TEMP ************************************************************************")
# print(region_table_means_temp)
# print(region_table_means_temp[0])
# print(region_table_means_temp[1])
# print(region_table_means_temp[2])
# print("REGION_TABLE_MEANS *******************************")
# print(region_table_means)
# region_table_means = region_table_means_temp
# print("REGION_TABLE_MEANS *******************************")
# print(region_table_means[1])

# region_table_calcs = [['Region','CasesAll_Chg','C_HospYes_Calc_Chg','Deaths_Chg','Tests_Chg','Pct_Pos_Calc']]
# for i in range(1,len(region_table_means)):
#     cases_calc = round(region_table_means[i][6],2)
#     hosp_calc = round(region_table_means[i][7] + region_table_means[i][8],2)
#     deaths_calc = round(region_table_means[i][9],2)
#     negatives_calc = round(region_table_means[i][10],2)
#     tests_calc = round(cases_calc + negatives_calc,2)
#     pct_pos_calc = round(cases_calc / (cases_calc + negatives_calc) * 100, 1)
#     region_table_calcs.append([region_table_means[i][0],commas_place(cases_calc),commas_place(hosp_calc),commas_place(deaths_calc),commas_place(tests_calc),pct(pct_pos_calc)])
# print("REGION_TABLE_CALCS *******************************")
# print(region_table_calcs)

####################################################################################################################################################################


# date_str = '08212020'
# # From USF archive of DOH data. These compile stats from CSV. Each file is about 70 rows.
# url_step1 = "https://covid19-usflibrary.hub.arcgis.com/datasets/florida-covid19-" + date_str + "-bycounty-csv"
# url = url_step1
# print(url)

# # Extract the long string from the website that identifies the file name.
# try:
#     response = requests.get(url)
#     response.raise_for_status()
# except:
#     print("Download problem on " + date_f)

# q = 'content="https://covid19-usflibrary.hub.arcgis.com/404' not in response.text[0:2000]
# print(q)

# date_list = []
# date_max_csv = '08/15/2020'
# start = datetime.datetime.strptime(date_max_csv, '%m/%d/%Y') + datetime.timedelta(days=1)
# # print('\nSTART: ',start)

# # If the CSV file is already updated to today, then skip all the dating information. CAREFUL:
# if datetime.datetime.strptime(date_max_csv, '%m/%d/%Y').date() != datetime.date.today():
#     end = datetime.date.today() - datetime.timedelta(days=1)
#     # end = datetime.datetime.strptime('08062020', '%m%d%Y')
#     days_iter = end.toordinal() - start.toordinal()
# else:
#     days_iter = 0

# # Iterate over the days from start to end
# for dayNum in range(0, days_iter + 1):
#     date = start + datetime.timedelta(days=dayNum)
#     date_str = datetime.datetime.strftime(date, '%m%d%Y')
#     # print('\nDATE_STR: ',date_str)
#     # Format the date appropriately
#     date_f = date.strftime('%m/%d/%Y')
#     # Add each date to date_list
#     date_list.append(date_f)
# print(date_list)
# date_list.remove('08/21/2020')
# print(date_list)

try:
    data_fl = pd.read_csv('covidfl.csv', delimiter=',', quotechar="'",  header=0)
except:
    print('covidfl.csv file does not exist')

date_max_csv = data_fl['Date'].max()
# print('\nDATE_MAX_CSV: ',date_max_csv)

day0_data = data_fl[(data_fl.Region == 'Collier') & (data_fl.Date == '08/28/2020')][['Region','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].groupby('Region').sum()

day1_data = data_fl[(data_fl.Region == 'Collier') & (data_fl.Date == '08/27/2020')][['Region','CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].groupby('Region').sum()
print(day0_data, day1_data)

# temp = 0
# if temp == 0:
#     date_max_csv = data_fl['Date'].max()
#     # print('\nDATE_MAX_CSV: ',date_max_csv)

#     start = datetime.datetime.strptime(date_max_csv, '%m/%d/%Y') + datetime.timedelta(days=1)
#     # print('\nSTART: ',start)

#     # If the CSV file is already updated to today, then skip all the dating information.
#     if datetime.datetime.strptime(date_max_csv, '%m/%d/%Y').date() != datetime.date.today():
#         # determine if the end date is today (if no 404 error) or yesterday (if 404 error)
#         if temp == 0:
#             #######################################
#             today = datetime.datetime.strftime(datetime.date.today(), '%m%d%Y')
#             print(today)
#             url = "https://covid19-usflibrary.hub.arcgis.com/datasets/florida-covid19-" + today + "-bycounty-csv"
#             try:
#                 response = requests.get(url)
#                 response.raise_for_status()
#             except:
#                 print("Download problem on " + date_f)
#             # print(response.text)

#             http_code = response.text

#             # Checks to make sure that the URL gives us data, not a 404. If it's good, we will proceed with parsing the file and reading and writing the csv
#             if 'content="https://covid19-usflibrary.hub.arcgis.com/404' not in http_code[0:2000]:
#                 end = datetime.date.today()
#             else:
#                 end = datetime.date.today() - datetime.timedelta(days=1)
#         #######################################
#         end = datetime.date.today()
#         # end = datetime.date.today() - datetime.timedelta(days=1)
#         # end = datetime.datetime.strptime('08062020', '%m%d%Y')
#         days_iter = end.toordinal() - start.toordinal()
#     else:
#         days_iter = 0
