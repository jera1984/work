# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 09:09:52 2016

@author: JXR8
"""

import pandas as pd
import matplotlib.style as st
import matplotlib.pyplot as plt
from collections import Counter
st.use('ggplot')

#df = pd.read_csv('Pt 21 ROE Dump.csv',usecols=['P21_NO','RPT_DT','FACILITY','LICENSEE_NAME'],parse_dates=['RPT_DT'],date_parser=lambda x: pd.datetime.strptime(x,'%m/%d/%Y %H:%M:%S')).fillna('')
df = pd.read_csv('part21ROEDump.csv',usecols=['P21_NO','RPT_DT','FACILITY','LICENSEE_NAME'],parse_dates=['RPT_DT'],date_parser=lambda x: pd.datetime.strptime(x,'%m/%d/%Y %H:%M:%S')).fillna('')
licensees = Counter(df['LICENSEE_NAME'].values).most_common()
temp = df['LICENSEE_NAME'].apply(lambda x: x.split(', ')).values
lics = []
for i in temp:
    lics += i
lics = sorted(list(set(lics)))
fac = sorted(list(set(df['FACILITY'].values)))

df['RPT_DT'] = df['RPT_DT'].apply(lambda x: x.year)
count = df.groupby(['RPT_DT']).size()

plt.cla()
count.plot(kind='bar', figsize=(12,5))
plt.xlabel('Year')
plt.ylabel('Count of Reports')
plt.title('Part 21 Reports (2005-Present)')



