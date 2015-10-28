# -*- coding: utf-8 -*-
"""

@author: alexey
"""
from preprocessing import prepare_texts
from term_document_counter import build_term_document_matrix
from term_document_counter import show_frequent_terms

wd = "C:/Users/Alexey/Documents/PyLSA_data"
encoding="utf-8"


prepare_texts(wd, min_word_lenght=3, use_lemmatization=True, use_stopwords=True, overwrite=False, encoding=encoding)

term_count_result = build_term_document_matrix(wd=wd, encoding=encoding)

matrix = term_count_result[0]
terms = term_count_result[1]
docs = term_count_result[2]

show_frequent_terms(20, terms, matrix)
