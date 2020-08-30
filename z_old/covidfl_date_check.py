import pandas as pd
import datetime

# Check to see that covidfl.csv exists.
try:
    data_fl = pd.read_csv('covidfl.csv', delimiter=',', quotechar="'",  header=0)
except:
    print('covidfl.csv file does not exist')

date_max_csv = data_fl['Date'].max()
print(date_max_csv)

# Initialitze the date list
date_list = list(data_fl['Date'].unique())
print('\nDATE_LIST: ',date_list)
# Check to see that covidfl.csv exists.
try:
    data_fl = pd.read_csv('covidfl.csv', delimiter=',', quotechar="'",  header=0)
except:
    print('covidfl.csv file does not exist')

date_max_csv = data_fl['Date'].max()
print(date_max_csv)

# Initialitze the date list
date_list = list(data_fl['Date'].unique())

print('\nDATE_LIST: ',date_list)

start = datetime.datetime.strptime(date_max_csv, '%m/%d/%Y') + datetime.timedelta(days=1)

# If the CSV file is already updated to today, then skip all the dating information. CAREFUL:
if datetime.datetime.strptime(date_max_csv, '%m/%d/%Y').date() != datetime.date.today():
    end = datetime.date.today() - datetime.timedelta(days=1)
    # end = datetime.datetime.strptime('08062020', '%m%d%Y')
    days_iter = end.toordinal() - start.toordinal()

print(start, end, days_iter)

######################################

region = 'Collier'
date_last_str = '08/17/2020'

# Panda pull of data by region and date(x)
day0_data = data_fl[(data_fl.Region == region) & (data_fl.Date == date_last_str)][['CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].values.tolist()
print(day0_data)