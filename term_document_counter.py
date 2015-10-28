# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 15:13:05 2015

@author: Alexey
"""
import scipy
from preprocessing import index_texts

def build_term_document_matrix(wd, encoding):
    
    # Following variables are used to incrementally count terms in each text
    # They are global to let subfunction increment.
    # terms_list contains all terms in corpora
    # terms_in_docs_freqs_list is list of lists. Each list inside corresponds
    # to each document and contains frequencies of terms in it. They are
    # sorted by first occurence of terms so can be of various lenght.
    
    global terms_list, files_list, terms_in_docs_freqs_list
    terms_in_docs_freqs_list = []
    
    dir_lemm = wd + "/texts_lemmatized/"
    
    files_list = index_texts(dir_lemm)
    
    print "Counting terms in texts..."
    
    counter=0
    lenght = str(len(files_list))
    terms_list = []
    
    for text_name in files_list:
        counter += 1  
        with open(dir_lemm + text_name) as text_reader:
            text = text_reader.read().decode(encoding)
            
            count_terms_in_text(text)
            
            print str(counter) + "/" + lenght + " files counted"
            
            #if counter % 100:
            #    print str(counter) + " files counted"
 
            

    print "Building term-document matrix..."
    matrix = scipy.sparse.lil_matrix((len(terms_list), len(files_list)), dtype="int16")
    for i in terms_in_docs_freqs_list:
        for j, n in enumerate(i):
            matrix[j, terms_in_docs_freqs_list.index(i)] = terms_in_docs_freqs_list[terms_in_docs_freqs_list.index(i)][j]
    
    print "Done."
    return matrix, terms_list, files_list
    

def count_terms_in_text(text):
    
    global terms_list
    global terms_in_docs_freqs_list
    
    terms_in_text = []
    
    terms_in_text_freq = {}        
    
    terms_in_text_freq_list = []
    
    for term in text.split():
        
        # Adding term to main list of terms
        if term not in terms_list:
            terms_list.append(term)
        
        # Counting frequency of terms in this text
        if term not in terms_in_text:
            terms_in_text.append(term)
            terms_in_text_freq[term]=1
        else:
            terms_in_text_freq[term]+=1
                
    for term in terms_list:
        # Constructing list of frequencies of terms in text 
        if term in terms_in_text:
            terms_in_text_freq_list.append(terms_in_text_freq[term])
        else:
            terms_in_text_freq_list.append(0)
            
    terms_in_docs_freqs_list.append(terms_in_text_freq_list)        
 
def show_frequent_terms(number,terms_list, matrix):
    term_freq={}
    for i,j in enumerate(terms_list):
        term_freq[j]=sum(matrix.data[i])

    for key, value in sorted(term_freq.iteritems(), key=lambda (k,v): (v,k))[-number-1:-1]:
        print key, int(value)   
  

    


## Needs reworking

#def TermFreqByDoc(docnumber, number):
#    term_freq={}
#    for i,j in enumerate(terms):
#        term_freq[j]=dtm.data[i]
#    for key, value in sorted(term_freq.iteritems(), key=lambda (k,v): (v,k))[-number-1:-1]:
#        print key, int(value)

