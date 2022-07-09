import csv
import pandas as pd
import pickle

dictionary = {}
sentences_merged = []

def isMainWord(a):
    flag = True
    if a == '\n':
        return False
    for i in a:
        if(not i.isupper() and not (i == '\n') and not i.isalpha()):
            flag = False
            break
    return flag


def mergeSentences(l):
    i = 0
    temp_string = ""
    while i < len(l):
        if isMainWord(l[i]):
            temp_string = l[i].replace("\n","")
            print(f">>> {temp_string}")
            sentences_merged.append(temp_string)
            temp_string = ""
            i = i + 1
        elif l[i] != '\n':
            while i < len(l) and l[i] != '\n':
                temp_string = temp_string + l[i].replace("\n"," ")
                i = i + 1
            sentences_merged.append(temp_string)
            print(f">> {temp_string}")
            temp_string = ""
        else:
            i = i + 1
    with open('files/mergedSentences.pkl', 'wb') as f:
        pickle.dump(sentences_merged, f)

'''
#To Retrieve the list: 
    with open('files/mergedSentences.pkl', 'rb') as f:
        sentences_merged = pickle.load(f)
'''
'''
def open_read():
    with open('files/mainSentences.pkl', 'rb') as f:
        all_main_words = pickle.load(f)
    print(all_main_words)
'''

def read_file():
    fp = open("dictionary.txt","r")
    all_strings = fp.readlines()
    all_main_words = []
    for i in all_strings:
        if isMainWord(i):
            all_main_words.append(i.replace("\n",""))
    with open('files/mainWords.pkl', 'wb') as f:
        pickle.dump(all_main_words, f)
    mergeSentences(all_strings)


# read_file()
read_file()