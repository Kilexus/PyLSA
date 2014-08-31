# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 10:12:08 2014

@author: alexey
"""
import re, os, pymorphy2, numpy as np

dir="/home/alexey/Python/"
#text= dir + name

stopwords_path = "/home/alexey/Python/LSA/stopwords.txt"


min_word_lenght=4


def Processor():
    global terms, term_index, docs, docs_index, stop_words, files_list, dtm
    terms=[]
    docs=[]
    dtm=[]
    stop_words = set(line.strip() for line in open(stopwords_path))
    for t in files_list:
        print "Processing " + t
        docs.append(t)
        with open(dir + t) as t:
            t = t.read()
        t = CleanText(t)
        t = Lemmatizer(t)
        TDCounter(t)
    ConstructDTM()
    print "Done."

def IndexTexts(dir):
    global files_list
    files_list = []
    for f in os.listdir(dir):
        if os.path.isfile(dir + f): 
            files_list.append(f)
    return files_list


def CleanText(t):
    t = re.sub('\-\s\r\n\s{1,}|\-\s\r\n|\r\n', '', t) #deleting newlines and line-breaks
    t = re.sub('[.,:;%©?*,!@#$%^&()\d]|[+=]|[[]|[]]|[/]|"|\s{2,}|-', ' ', t) #deleting symbols
    t = unicode(t, errors='replace')
    t = " ".join(word.decode('utf-8').lower() for word in t.split() if len(word)>=min_word_lenght*2) #lowercasing and removing short words
    t = " ".join(word for word in t.split() if word not in stop_words) # stopwords
    return t

def Lemmatizer(t):
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
    m = np.zeros((len(terms), len(docs)))
    for i in dtm:
        for j, n in enumerate(i):
            m[j][dtm.index(i)] = dtm[dtm.index(i)][j]
    dtm = m
    
def TermFreqTop(number):
    term_freq={}
    for i,j in enumerate(terms):
        term_freq[j]=np.sum(dtm[i])

    for key, value in sorted(term_freq.iteritems(), key=lambda (k,v): (v,k))[-number-1:-1]:
        print key, int(value)

def TermFreqByDoc(docnumber, number):
    term_freq={}
    for i,j in enumerate(terms):
        term_freq[j]=np.sum(dtm[i,docnumber])
    for key, value in sorted(term_freq.iteritems(), key=lambda (k,v): (v,k))[-number-1:-1]:
        print key, int(value)


IndexTexts(dir)
Processor()
#TermFreqByDoc(4, 10)



#for i in terms:
#    print i, terms.index(i)


#for item in sorted_term_freq:
#    print item

#for i,j in sorted_ti:
#    print i,j

#print type(sorted_tf)
#for m in sorted_term_freq:
#    print m
    
#print sorted_term_freq



#d = {'key{}'.format(n): 'value{}'.format(n) for n in xrange(3)}
#table =  '\t'.join(['{}\t{}'.format(d.get(k), k) for k in sorted(d)])

#print repr(sorted_tf).decode("unicode-escape")
