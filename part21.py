# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 17:02:21 2016

@author: Jesse
"""

from bs4 import BeautifulSoup
import csv

fileName = 'part21rpts-1994-1977.html'

html = open(fileName, 'r').read()
soup = BeautifulSoup(html, 'lxml')

tables = soup.find_all('table')

results = []
rowdata = []

for table in tables:
    for row in table.find_all('tr'):
        for cell in row.find_all('td'):
            rowdata.append(cell.text)
        results.append(rowdata)
        rowdata = []
        
with open('part21data.csv', 'w') as f:
    cwriter = csv.writer(f)
    cwriter.writerow(results[0])
    for row in results:
        if 'LOG_' not in row[0]:
            cwriter.writerow(row)