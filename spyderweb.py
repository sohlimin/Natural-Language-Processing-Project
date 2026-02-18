#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 21:11:28 2026

@author: cxvumuh
"""

#The first argument is a string containing the filename. 
#The second argument is another string containing a few characters 
#describing the way in which the file will be used. 
#mode can be 'r' when the file will only be read.
#https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files



import pandas

with open('Nenets_interlinear_gloss.htm', 'r') as file:
    file_guts = file.read()

type(file_guts)

separated_by_ref = file_guts.split("<span class=\"ref\">")[1:] #sliced to remove element 0

separated_by_ref[0]

cyrillic_transliteration = separated_by_ref[0].split('<span class=\"st\">')[1].split('</span>')[0]

cyrillic_transliteration

def parseout_span_contents(class_id, sections):
    contents = []
    for section in sections:
        contents.append(section.split(f'<span class=\"{class_id}\">')[1].split('</span>')[0])
    return contents

cyr_translit = parseout_span_contents('st', separated_by_ref)
lat_translit = parseout_span_contents('ts', separated_by_ref)
eng_translat = parseout_span_contents('ft', separated_by_ref)
rus_translat = parseout_span_contents('fr', separated_by_ref)
ger_translat = parseout_span_contents('fg', separated_by_ref)

#this works
#all_tables = pandas.read_html(file_guts)

from io import StringIO

def parseout_tables(sections):
    tables = []
    for section in sections:
        table = section.split('<table>')[1].split('</table>')[0]
        tables.append(pandas.read_html(StringIO(f'<table>{table}</table>'))[0])
    return tables

all_tables = parseout_tables(separated_by_ref)

all_tables[0]

all_tables[0].loc[:,0] #why comma - numeric indexing not names, so this will ALWAYS grab the first column

all_tables[0].shape[1]

# Making a list of list of dictionaries for all tables
listOfSentencesOfStory = []
for j in range(0, len(all_tables)):
    #Getting a list of dictionaries but a single table
    listOfWordsInASentence = []
    for i in range(0, all_tables[j].shape[1]):
        dictionary_ofWordInfo = {
            "phonemic": all_tables[j].loc[0, i],
            "pos_tag": all_tables[j].loc[3, i],
            "Russian": all_tables[j].loc[4, i],
            "English": all_tables[j].loc[5, i],
            "German": all_tables[j].loc[6, i],
        }
        listOfWordsInASentence.append(dictionary_ofWordInfo)
    listOfSentencesOfStory.append(listOfWordsInASentence)

listOfSentencesOfStory[0]

#Attempt 1
# Making a list of dictionaries, where each corresponds to a sentence
listOfSentencesOfStory = []
for j in range(0, len(separated_by_ref)): #for every sentence j...
    #First create from sentence j's table, a LIST of dictionaries(ofWordInfo) 
    listOfWordsInASentence = []
    for i in range(0, all_tables[j].shape[1]):
        dictionary_ofWordInfo = {
            "phonemic": all_tables[j].loc[0, i],
            "pos_tag": all_tables[j].loc[3, i],
            "Russian": all_tables[j].loc[4, i],
            "English": all_tables[j].loc[5, i],
            "German": all_tables[j].loc[6, i],
        }
        listOfWordsInASentence.append(dictionary_ofWordInfo)
    
    #Secondly, create a dictionary per sentence j
    #Put that list inside, along with sentence j's standalone transliterations andtranslations
    dictionary_forASingleSentence =  {
        "cyrillic_transliteration" : cyr_translit[j],
        "latin_transliteration" : lat_translit[j],
        "Russian_translation" : rus_translat[j],
        "English_translation" : eng_translat[j],
        "German_translation" : ger_translat[j],
        "wordInfo_dictionary" : listOfWordsInASentence
    }
    listOfSentencesOfStory.append(dictionary_forASingleSentence)

eng_translat[0].find("river")

query = {
    'cyr_translit': None,
    'lat_translit': None,
    'rus_translat': None,
    'eng_translat': "river",
    'ger_translat': None,
    'wordInfo_dictionary': {
        'phonemic': "jaxa",
        'pos_tag': None,
        'Russian': None,
        'English': "-1SG",
        'German': None
    }
}

for sentence in listOfSentencesOfStory:
    break

sentence["English_translation"].find("river")

sentence

query = {
    'cyr_translit': None,
    'lat_translit': None,
    'rus_translat': None,
    'eng_translat': "river",
    'ger_translat': None,
    'wordInfo_dictionary': {
        'phonemic': ["jaxa"],
        'pos_tag': None,
        'Russian': None,
        'English': ["-1SG"],
        'German': None
    }
}

print("exists in sentence indexes: ", end='')
def doSearch(query):
    matching_sentences = []
    for i in range(len(listOfSentencesOfStory)):
        sentence = listOfSentencesOfStory[i]

        keep_this_sentence = True

        if query['cyr_translit'] is not None:
            if sentence["cyrillic_transliteration"].find(query['cyr_translit']) == -1:
                keep_this_sentence = False
        if query['lat_translit'] is not None:
            if sentence["latin_transliteration"].find(query['lat_translit']) == -1:
                keep_this_sentence = False
        if query['rus_translat'] is not None:
            if sentence["Russian_translation"].find(query['rus_translat']) == -1:
                keep_this_sentence = False
        if query['eng_translat'] is not None:
            if sentence["English_translation"].find(query['eng_translat']) == -1:
                keep_this_sentence = False
        if query['ger_translat'] is not None:
            if sentence["German_translation"].find(query['ger_translat']) == -1:
                keep_this_sentence = False
        for key in query['wordInfo_dictionary'].keys():
            if query['wordInfo_dictionary'][key] is not None:
                for word in query['wordInfo_dictionary'][key]:
                    if word not in [dictionary[key] for dictionary in sentence['wordInfo_dictionary']]:
                        keep_this_sentence = False

        if keep_this_sentence:
            matching_sentences.append(sentence)
    return matching_sentences
doSearch(query)

def input_query():
    query = {
        'cyr_translit': input("Cyrillic transliteration:"),
        'lat_translit': input("Latin transliteration:"),
        'rus_translat': input("Russian transliteration:"),
        'eng_translat': input("English transliteration:"),
        'ger_translat': input("German transliteration:"),
        'wordInfo_dictionary': {
            'phonemic': input("Phonemic transliteration:").split(),
            'pos_tag': input("POS tagging:"),
            'Russian': input("Russian transliteration:"),
            'English': input("English transliteration:"),
            'German': input("German transliteration:")
        }
    }
    return query

def main_screen():
    print("Welcome to Nenets Corpus Search! Enter your query below:")
    query = input_query()
    search_results = doSearch(query)
    print(f"There are {len(search_results)} search results for your query!")
    for search_result in search_results:
        print(f"Cyrillic transliteration: {search_result['cyrillic_transliteration']}")
        print(f"Latin transliteration: {search_result['latin_transliteration']}")
        print(f"Russian translation: {search_result['Russian_translation']}")
        print(f"English translation: {search_result['English_translation']}")
        print(f"Phonemic tagging: {' '.join([i['phonemic'] for i in search_result['wordInfo_dictionary']])}")
        print(f"POS tagging: {' '.join([i['pos_tag'] for i in search_result['wordInfo_dictionary']])}")
        print(f"Russian tagging: {' '.join([i['Russian'] for i in search_result['wordInfo_dictionary']])}")
        print(f"English tagging: {' '.join([i['English'] for i in search_result['wordInfo_dictionary']])}")
        print(f"German tagging: {' '.join([i['German'] for i in search_result['wordInfo_dictionary']])}")
        print()

main_screen()