# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 08:15:44 2016

@author: JXR8
"""

from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
import time
import datetime
import re
import PyPDF2
import io
import os

logRegex = re.compile('\d+-\d+(-\d+)?')

def get_content(url):
    with requests.Session() as s:
        r = s.get(url)
        c = r.content
    s.close()
    return c
    
class PageText:
    def __init__(self, url='', logno=''):
        self.url = url
        self.logno = logno
        self.text = ''
        self.year = self.logno[:4]
        self.content = get_content(self.url)
    
    def get_text(self):
        if self.url.endswith('.html'):
            soup = BeautifulSoup(self.content, 'lxml')
            body = soup.find('div',{'id':'mainSubFull'})
            if not body:
                return self
            bcrumb = body.find('div', {'class':'bcrumb'})
            if bcrumb:
                bcrumb.decompose()
            update = body.find('div', {'style':'padding:1.5em 0; font:.88em'})
            if update:
                update.decompose()
            self.text = str(body.text)
            return self
        
        elif self.url.endswith('.pdf'):
            data = io.BytesIO(self.content)
            try:
                reader = PyPDF2.PdfFileReader(data)
                for pageNum in range(reader.numPages):  # Loop through pages
                    self.text += ' ' + reader.getPage(pageNum).extractText()
            except:
                return self
            return self
        
        elif re.search('en\d+$', self.url):
            ennum = self.url[-7:]
            soup = BeautifulSoup(self.content, 'lxml')
            temp = ''
            cursor = soup.find('a', {'name':ennum})
            try:
                while cursor != None:
                    temp += str(cursor)
                    cursor = cursor.next_sibling
                    if cursor != None and type(cursor) != NavigableString and 'name' in cursor.attrs.keys():
                        break
                self.text += BeautifulSoup(temp, 'lxml').text.strip()                    
                return self
            except:
                return self
        else:
            return self
    
    def write_text(self):
        directory = 'textfiles/' + self.year
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory + '/' + self.logno + '.txt', 'w', encoding='utf-8') as file:
            file.write(self.text)

check = []
years = range(2014,datetime.datetime.now().year + 1)
baseurl = 'http://www.nrc.gov/reading-rm/doc-collections/event-status/part21/'
year = 1995

for year in years:
    url = baseurl + str(year) + '/'
    html = get_content(url)
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('table')[1]
    now = time.time()
    for link in table.find_all('a'):
        log = re.search(logRegex, link.text)
        if log:
            logno = log.group()
            url = 'http://www.nrc.gov' + link.get('href')
            if len(link.get('href')) < 20:
                url = 'http://www.nrc.gov/reading-rm/doc-collections/event-status/part21/' + str(year) + '/' + link.get('href')
            page = PageText(url, logno)
            page.get_text().write_text()
            if page.text == '':
                check.append(logno)
    print('Completed {} in {} seconds. '.format(year, time.time() - now))      