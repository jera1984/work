# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 09:19:14 2016

@author: JXR8
"""
import string
import os
from nltk.corpus import stopwords

def text_process(mess):
    """
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove all stopwords
    3. Returns a list of the cleaned text
    """
    # Check characters to see if they are in punctuation and join the characters again to form the string.
    nopunc = ''.join([char for char in mess if char not in string.punctuation])

    # Now just remove any stopwords
    return ' '.join([word.lower() for word in nopunc.split() if word.lower() not in stopwords.words('english') and len(word) > 2])

textwd = os.getcwd() + '\\textfiles'
files = [fileList for dirName, subdirList, fileList in os.walk(os.getcwd() + '\\textfiles')]
files = ' '.join([' '.join([f for f in file]) for file in files]).split()

for file in files:
    with open('text\\' + file, 'w', encoding='utf-8') as f1:
        with open(textwd + '\\' + file[:4] + '\\' + file, encoding='utf-8') as f2:
            f1.write(text_process(f2.read()))