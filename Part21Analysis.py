# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 08:13:38 2016

@author: JXR8
"""
#import nltk
from time import time
from nltk.corpus import stopwords
import string
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
#import matplotlib.pyplot as plt


def text_process(text):
    return text.split()

print('Getting data from text files...')
t0 = time()
files = [fileList for dirName, subdirList, fileList in os.walk(os.getcwd() + '\\text')][0]
#files = ' '.join([' '.join([f for f in file]) for file in files]).split()
documents = []
for doc in files:
    with open(os.getcwd() + '\\text\\' + doc,'r',encoding='utf-8') as f:
        documents.append(f.read())
print("done in %0.3fs." % (time() - t0))

print('Generating bag of words and vectorizing...')
t0 = time()
bow_transformer = CountVectorizer(analyzer=text_process).fit(documents)
document_bow = bow_transformer.transform(documents)
names = bow_transformer.vocabulary_
print("done in %0.3fs." % (time() - t0))

print('Generating tfidf...')
t0 = time()
tfidf_transformer = TfidfTransformer().fit(document_bow)
#print(tfidf_transformer.idf_[bow_transformer.vocabulary_['pump']])
document_tfidf = tfidf_transformer.transform(document_bow)
print("done in %0.3fs." % (time() - t0))

print('Shape of Sparse Matrix: ', document_bow.shape)
print('Amount of Non-Zero occurences: ', document_bow.nnz)
print('sparsity: %.2f%%' % (100.0 * document_bow.nnz / (document_bow.shape[0] * document_bow.shape[1])))
vectorizer = TfidfVectorizer(min_df=1,max_features=100,stop_words="english")

tfidf = vectorizer.fit_transform(documents)
#nmf = NMF(n_components=10).fit(tfidf)
nmf = NMF(n_components=10,random_state=1, alpha=.1, l1_ratio=.5).fit(tfidf)

feature_names = vectorizer.get_feature_names()

for topic_idx, topic in enumerate(nmf.components_):
    print("Topic #%d: " %topic_idx)
    print(' '.join([feature_names[i] for i in topic.argsort()[:-10 -1:-1]]))
    print('\n')