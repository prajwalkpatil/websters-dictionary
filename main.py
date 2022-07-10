import csv
import pandas as pd
import pickle
import json

dictionary = {}
all_main_words = []
sentences_merged = []

def is_main_word(a):
    a = a.replace("\n","")
    flag = True
    if a == '':
        return False
    if a == '\n':
        return False
    for i in a:
        if not ((i >= 'A' and i <= 'Z') or (i == ' ' or i == ';')):
            flag = False
            break
    return flag


def merge_sentences(l):
    i = 0
    temp_string = ""
    while i < len(l):
        if is_main_word(l[i]):
            temp_string = l[i].replace("\n","")
            # print(f">>> {temp_string}")
            sentences_merged.append(temp_string)
            temp_string = ""
            i = i + 1
        elif l[i] != '\n':
            while i < len(l) and l[i] != '\n':
                temp_string = temp_string + l[i].replace("\n"," ")
                i = i + 1
            sentences_merged.append(temp_string)
            # print(f">> {temp_string}")
            temp_string = ""
        else:
            i = i + 1
    with open('files/mergedSentences.pkl', 'wb') as f:
        pickle.dump(sentences_merged, f)

def read_main_words_file():
    with open('files/mainWords.pkl', 'rb') as f:
        all_main_words = pickle.load(f)
    return all_main_words

def read_merged_sentences_file():
    with open('files/mergedSentences.pkl', 'rb') as f:
        sentences_merged = pickle.load(f)
    return sentences_merged


def read_file():
    fp = open("dictionary.txt","r")
    all_strings = fp.readlines()
    for i in all_strings:
        if is_main_word(i):
            all_main_words.append(i.replace("\n",""))
    with open('files/mainWords.pkl', 'wb') as f:
        pickle.dump(all_main_words, f)
    merge_sentences(all_strings)

def make_dictionary(sentences_merged):
    i = 0
    while i < len(sentences_merged):
        if is_main_word(sentences_merged[i]):
            key_word = sentences_merged[i]
            i = i + 1 
            if key_word not in dictionary: 
                dictionary.update({key_word : []})
            dictionary[key_word].append({'et' :"", 'meanings':[]})
            last_index = len(dictionary[key_word]) - 1
            dictionary[key_word][last_index]['et'] = sentences_merged[i]
            i = i + 1
            while i < len(sentences_merged) and not is_main_word(sentences_merged[i]):
                if sentences_merged[i] != '\n':
                    dictionary[key_word][last_index]['meanings'].append(sentences_merged[i])
                i = i + 1
            '''
            print(f">> {key_word}")
            print(dictionary[key_word]) 
            print("\n")
            '''
        i = i + 1
    jsonString = json.dumps(dictionary)
    jsonFile = open("files/Dictionary.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()
    return dictionary

def read_dictionary():
    with open("files/Dictionary.json") as file:
        dictionary = json.load(file)
    return dictionary


class TrieNode:
    def __init__(self, char):
        self.char = char
        self.is_end = False
        self.counter = 0
        self.children = {}


class Trie(object):
    def __init__(self):
        self.root = TrieNode("")
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node
        node.is_end = True
        node.counter += 1
        
    def dfs(self, node, prefix):
        if node.is_end:
            self.output.append((prefix + node.char, node.counter))
        
        for child in node.children.values():
            self.dfs(child, prefix + node.char)
        
    def query(self, x):
        self.output = []
        node = self.root
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                return []
        self.dfs(node, x[:-1])
        return sorted(self.output, key=lambda x: x[1], reverse=True)

def insert_main_words():
    dictionary_trie = Trie()    
    for i in all_main_words:
        dictionary_trie.insert(i)
    return dictionary_trie

def main():
    read_file()
    dictionary = make_dictionary(sentences_merged)
    print(all_main_words)
    dictionary_trie = insert_main_words()
    print(dictionary_trie.query("JAGA"))

main()
