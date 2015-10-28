# -*- coding: utf-8 -*-
"""

@author: alexeyknorre
"""
import os
import re
import pymorphy2




def index_texts(dir_texts):
    print "Indexing files..."
    if not os.path.isdir(dir_texts):
        raise Exception("There is no text directory.")
    files_list = []
    for f in os.listdir(dir_texts):
        if os.path.isfile(dir_texts + f) and f.lower().endswith('.txt'): 
            files_list.append(f)
    print "There are "+str(len(files_list))+" files."
    if files_list == []:
        raise Exception("Texts directory is empty.")
    else:
        return files_list

def preprocess_text(text, min_word_lenght, use_lemmatization, use_stopwords, stopwords, encoding):
    global morph
    text = text.decode(encoding)
    text = re.sub('\-\s\r\n\s{1,}|\-\s\r\n|\r\n', '', text) #deleting newlines and line-breaks
    text = re.sub('[.,:;%©?*,!@#$%^&()\d]|[+=]|[[]|[]]|[/]|"|\s{2,}|-', ' ', text) #deleting symbols
    text = " ".join(word.lower() for word in text.split() if len(word)>=min_word_lenght) #lowercasing and removing short words
    if use_stopwords and stopwords:
        text = " ".join(word for word in text.split() if word not in stopwords) # stopwords
    if use_lemmatization:
        text = " ".join(morph.parse(word)[0].normal_form for word in text.split())
    return text

def prepare_texts(wd, min_word_lenght, use_lemmatization=True, use_stopwords=True, encoding="utf-8", overwrite=False):
    global morph
    
    dir_texts= wd + "/texts/"

    stopwords_path = wd + "/stopwords.txt"    
    
    files_list = index_texts(dir_texts)
    dir_lemm =  dir_texts[:-1] + "_lemmatized/"
    if use_stopwords:
        if not os.path.isfile(stopwords_path):
            stopwords = False
            print "Stopwords NOT found. Proceeding without stopwords cleaning stage..."
        else:
            with open(stopwords_path,"r") as stopwords_reader:
                stopwords = stopwords_reader.read().decode("utf-8")
    else:
        stopwords = False
            
    counter = 0
    morph = pymorphy2.MorphAnalyzer()
    if not os.path.exists(dir_lemm):
        os.makedirs(dir_lemm)
    for f in files_list: #Create lemmatized files
        counter += 1    
        if not overwrite:
            if not os.path.isfile(dir_lemm + f):
                print str(counter)+"/"+str(len(files_list)) +" Preprocessing " + f + "... "
                with open(dir_texts + f) as text_reader:
                    text = text_reader.read()
                text = preprocess_text(text, min_word_lenght, use_lemmatization, use_stopwords, stopwords, encoding)
                with open(dir_lemm + f,'w') as f:
                    f.write(text.encode("utf-8"))
            else:
                print str(counter)+"/"+str(len(files_list)) +" Skip already lemmatized " + f + "... "
        else:
            print str(counter)+"/"+str(len(files_list)) +" Preprocessing " + f + "... "
            with open(dir_texts + f) as text_reader:
                text = text_reader.read()
            text = preprocess_text(text, min_word_lenght, use_lemmatization, use_stopwords, stopwords, encoding)
            with open(dir_lemm + f,'w') as f:
                f.write(text.encode("utf-8"))

          
            
    print "Preprocessing completed."
		