import pandas as pd
import numpy as np

data_fl = pd.read_csv('covidfl.csv', delimiter=',', quotechar="'",  header=0)
print(data_fl.head(5))
# print(data_fl.info())
# a = data_fl[data_fl.DEPCODE == 21].County
# print(a)
# b = data_fl.groupby(['County', 'Date']).size()
# print(b)
# d = data_fl[(data_fl.County != 'State')].groupby('Date').size()
# d.to_csv('test1.csv')

# e = data_fl.pivot_table('CasesAll', index='County')
# # titanic.pivot_table('survived', index='sex', columns='class')
# e.to_csv('test1.csv')

#select column to convert to list here
# date_list = set(data_fl['Date'].tolist())
# print(date_list)
# print(max(date_list))
# print(type(date_last))
# date_prior = date_last - 1
# print(date_last)

h = []
date_last_str = '07/31/2020'
date_prior_str = '07/30/2020'
f = data_fl[(data_fl.County == 'Collier') & (data_fl.Date == date_last_str)][['CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].values.tolist()
f = f[0]
list_len = len(f)
print(f)
g = data_fl[(data_fl.County == 'Collier') & (data_fl.Date == date_prior_str)][['CasesAll','C_HospYes_Res','C_HospYes_NonRes','Deaths','T_negative']].values.tolist()
g = g[0]
print(g)

for i in range(list_len):
    h.append(f[i] - g[i])
# This gives the differences between the last and the prior day's dates.
print(h)
