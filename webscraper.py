# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 07:26:58 2016

@author: JXR8
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import matplotlib.style as st
import matplotlib.pyplot as plt
import datetime
import re

datere = re.compile('[\d/]{2,}/(\d+)')
datere2 = re.compile('/\d{4}')


def parse_date(date):
    date = str(date)
    year = ''
    if re.search(datere, date):
        year = re.search(datere, date).group(1)
        if len(year) < 4:
            year = '19' + year
    elif re.search(datere2, date):
        year = re.search(datere2, date).group(1)
    else:
        print(date + ' could not be parsed')
        return 0
    return int(year)

#def check_year(date):
#    
   
years = range(1995,datetime.datetime.now().year + 1)
url = 'http://www.nrc.gov/reading-rm/doc-collections/event-status/part21/'
year = 1995
df = pd.DataFrame()
for year in years:
    html = requests.get(url + str(year) + '/').content
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.find_all('table')
    temp = pd.read_html(str(tables), flavor='bs4')[1].ix[1:]
    temp['year'] = year
    df = pd.concat([df,temp])



df.columns=['logno', 'notifier', 'description', 'reportdate', 'accession', 'year']
df = df[df['reportdate'].apply(lambda x: type(x)) == str]
#df = df.reset_index()


oldlist = pd.concat(pd.read_html('oldpart21s.html'))
oldlist = oldlist[oldlist[0] != 'LOG_NO']
oldlist = oldlist[oldlist[3] != 'REP_DAT E']
oldlist[5] = oldlist[3].apply(parse_date)
oldlist.columns=['logno', 'notifier', 'description', 'reportdate', 'accession', 'year']
df = pd.concat([df,oldlist])
count = df.groupby(['year']).size().drop(pd.datetime.now().year)

st.use('ggplot')
plt.cla()
count.plot(kind='bar', figsize=(12,5))
plt.xlabel('Year')
plt.ylabel('Count of Reports')
plt.title('Part 21 Reports (1977-{})'.format(pd.datetime.now().year - 1))
plt.show()

notifiers = set(df['notifier'].values)

newdf = df[df['notifier'].apply(lambda x: 'summer units 2 & 3' not in x.lower() and 'summer 2 & 3' not in x.lower() and 'north anna 3' not in x.lower() and 'watts bar unit 2' not in x.lower() and 'watts bar 2' not in x.lower() and 'summer units 2 & 3' not in x.lower() and 'vogtle units 3 & 4' not in x.lower() and 'cb&i' not in x.lower() and 'wectec' not in x.lower() and 'louisiana' not in x.lower() and 'mox' not in x.lower() and 'shaw' not in x.lower())&df['description'].apply(lambda x: 'ap 1000' not in x.lower() and 'ap1000' not in x.lower() and 'abwr' not in x.lower() and 'watts bar unit 2' not in x.lower())]
latestfixed = pd.DataFrame(pd.DataFrame(newdf[newdf['year'] > 1999]['logno'].apply(lambda x: '-'.join(x.split('-')[:2])).drop_duplicates())['logno'].apply(lambda x: x.split('-')[0])).groupby(['logno']).size()[:-1]
plt.cla()
latestfixed.plot(kind='bar', figsize=(12,5))
plt.xlabel('Year')
plt.ylabel('Count of Reports')
plt.title('Part 21 Reports (2000-{})'.format(pd.datetime.now().year - 1))
plt.show()

newdf = newdf[newdf['year'] > 2009]
newdf['logno'] = newdf['logno'].apply(lambda x: '-'.join(x.split('-')[:2]))
newdf.drop_duplicates(['logno'], inplace=True)
newdf.to_csv('needreview.csv', index=False)