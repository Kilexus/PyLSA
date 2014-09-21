# -*- coding: utf-8 -*-
"""

@author: alexey
"""
import re, os, pymorphy2, numpy as np, scipy
from scipy import sparse

dir="/home/alexey/Python/small_data/"
#Temporary directory for lemmatized files
dir_lemm = "/home/alexey/Python/small_lemmatized/"
#text= dir + name

stopwords_path = "/home/alexey/Python/PyLSA/stopwords.txt"


min_word_lenght=4


def Processor():
    global terms, term_index, docs, docs_index, stop_words, files_list, dtm
    terms=[]
    docs=[]
    dtm=[]
    stop_words = set(line.strip() for line in open(stopwords_path))
    print "Preprocessing files..."
    files_list = IndexTexts(dir)
    #Create lemmatizeed directory
    if not os.path.exists(dir_lemm):
        os.makedirs(dir_lemm)
    for t in files_list: #Create lemmatized files
        if not os.path.isfile(dir_lemm + t):
            print "Preprocessing " + t + "..."
            with open(dir + t) as t_text:
                t_text = t_text.read()
            t_text = Preprocessing(t_text)
            with open(dir_lemm + t,'w') as f:
                f.write(t_text)

            #Process lemmatized files
    files_list = IndexTexts(dir)
    print "Counting terms in texts..."
    c=1
    for t in files_list:
        
        t_name = t
        with open(dir_lemm + t) as t:
            t = t.read()
        docs.append(t)
        if c % 100 == True:
            print str(c-1) + " files counted"
        c += 1
        TDCounter(t)
    ConstructDTM()
    print "Done."

def IndexTexts(dir):
    files_list = []
    for f in os.listdir(dir):
        if os.path.isfile(dir + f) and f.lower().endswith('.txt'): 
            files_list.append(f)
    return files_list

def Preprocessing(t):
    #Cleaning text
        t = re.sub('\-\s\r\n\s{1,}|\-\s\r\n|\r\n', '', t) #deleting newlines and line-breaks
        t = re.sub('[.,:;%©?*,!@#$%^&()\d]|[+=]|[[]|[]]|[/]|"|\s{2,}|-', ' ', t) #deleting symbols
        t = unicode(t, errors='replace')
        t = " ".join(word.decode('utf-8').lower() for word in t.split() if len(word)>=min_word_lenght*2) #lowercasing and removing short words
        t = " ".join(word for word in t.split() if word not in stop_words) # stopwords
    #Lemmatizing text
        morph = pymorphy2.MorphAnalyzer()
        t = " ".join(morph.parse(unicode(word))[0].normal_form for word in t.split())
        return t
    

def TDCounter(t):
    global terms, docs, dtm
    dt={}
    dt_list=[]
    for term in t.split():
        if term not in terms:
            terms.append(term)
        else:
            pass
        if term not in dt:
            dt[term]=1
        else:
            dt[term]+=1
    for t in terms:
        if t in dt:
            dt_list.append(dt[t])
        else:
            dt_list.append(0)
    dtm.append(dt_list)
    
    
def ConstructDTM():
    global dtm
    print "Building term-document matrix..."
    m = scipy.sparse.lil_matrix((len(terms), len(docs)), dtype=int16)
    for i in dtm:
        for j, n in enumerate(i):
            m[j, dtm.index(i)] = dtm[dtm.index(i)][j]
    dtm = m
    
def TermFreqTop(number):
    term_freq={}
    for i,j in enumerate(terms):
        term_freq[j]=sum(dtm.data[i])

    for key, value in sorted(term_freq.iteritems(), key=lambda (k,v): (v,k))[-number-1:-1]:
        print key, int(value)

## Needs reworking

#def TermFreqByDoc(docnumber, number):
#    term_freq={}
#    for i,j in enumerate(terms):
#        term_freq[j]=dtm.data[i]
#    for key, value in sorted(term_freq.iteritems(), key=lambda (k,v): (v,k))[-number-1:-1]:
#        print key, int(value)


Processor()
TermFreqTop(10)

#TermFreqByDoc(4, 10)
