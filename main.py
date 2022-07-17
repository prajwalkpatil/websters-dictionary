# ---------------------------------------------------------------------------- #
#                     Webster's Dictionary - main functions                    #
# ---------------------------------------------------------------------------- #

# ------------------------------ Import packages ----------------------------- #
import csv
import pickle
import json
import string 

# ----------------------------- Global variables ----------------------------- #
#Dictionary containing all the words with their meanings
dictionary = {}
#A list containing all the main words
all_main_words = []
#A list containing all the single sentences merged by removing the newline chars  
sentences_merged = []
#A set containing all the word-recommendations
recommendations = set()

# ---------------------------------------------------------------------------- #
# -------------- Function to determine if a word is a main word -------------- #
# ---------------------------------------------------------------------------- #
#      Conditons for a word to be a main word as per the given text file,      #
#      - It should be on a single line.                                        #
#      - It should contain only uppercase letters.                             #
#      - It can contain spaces and semicolons.                                 #
# ---------------------------------------------------------------------------- #
def is_main_word(a):
    a = a.replace("\n","")
    flag = True
    if a == '':
        return False
    if a == '\n':
        return False
    for i in a:
        if not ((i >= 'A' and i <= 'Z') or (i == ' ' or i == ';') or i == '-' ):
            flag = False
            break
    return flag

# - Function to merge all the single sentences by removing the newline chars - #
def merge_sentences(l):
    i = 0
    temp_string = ""
    while i < len(l):
        #If it's a main word just append the word to the list 
        if is_main_word(l[i]):
            temp_string = l[i].replace("\n","")
            sentences_merged.append(temp_string)
            temp_string = ""
            i = i + 1
        #Append the sentences untill a seperate newline or mainword is encountered
        elif l[i] != '\n':
            while i < len(l) and l[i] != '\n':
                temp_string = temp_string + l[i].replace("\n"," ")
                i = i + 1
            sentences_merged.append(temp_string)
            temp_string = ""
        else:
            i = i + 1
    #Dump the merged sentences to a pickle file
    with open('files/mergedSentences.pkl', 'wb') as f:
        pickle.dump(sentences_merged, f)

# ---------- Function to read the pickle file containing main words ---------- #
def read_main_words_file():
    with open('files/mainWords.pkl', 'rb') as f:
        all_main_words = pickle.load(f)
    return all_main_words

# -------- Function to read a pickle file containing merged sentences -------- #
def read_merged_sentences_file():
    with open('files/mergedSentences.pkl', 'rb') as f:
        sentences_merged = pickle.load(f)
    return sentences_merged

# -- Function to read the given dictionary.txt file and find the main words -- #
def read_file():
    fp = open("dictionary.txt","r")
    all_strings = fp.readlines()
    for i in all_strings:
        #If its a main word then append it to the all_main_words
        if is_main_word(i):
            all_main_words.append(i.replace("\n",""))
    #Dump the main word to a pickle file
    with open('files/mainWords.pkl', 'wb') as f:
        pickle.dump(all_main_words, f)
    #Call merge_sentences to merge the sentences with newline
    merge_sentences(all_strings)

# ----------- Function to make dictionary from the merged sentences ---------- #
def make_dictionary(sentences_merged):
    i = 0
    while i < len(sentences_merged):
        if is_main_word(sentences_merged[i]):
            key_word = sentences_merged[i]
            i = i + 1 
            #If the key_word is not in the dictionary, update the dictionary
            if key_word not in dictionary: 
                dictionary.update({key_word : []})
            #Create a dictionary inside an array for each meaning of a word
            dictionary[key_word].append({'et' :"", 'meanings':[]})
            last_index = len(dictionary[key_word]) - 1
            #Insert etymology for a key_word
            dictionary[key_word][last_index]['et'] = sentences_merged[i]
            i = i + 1
            while i < len(sentences_merged) and not is_main_word(sentences_merged[i]):
                if sentences_merged[i] != '\n':
                    #Append meanings to the meaning array for a keyword
                    dictionary[key_word][last_index]['meanings'].append(sentences_merged[i])
                i = i + 1
        i = i + 1
    #Dump the dictionary to a JSON file
    jsonString = json.dumps(dictionary)
    jsonFile = open("files/Dictionary.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()
    return dictionary

# ---------------- Function to read dictonary from a JSON file --------------- #
def read_dictionary():
    with open("files/Dictionary.json") as file:
        dictionary = json.load(file)
    return dictionary

# ------------------- Class denoting each node of a Trie ------------------- #
class TrieNode:
    def __init__(self, char):
        self.char = char
        self.is_end = False
        self.counter = 0
        self.children = {}

# ----------- Trie class with the methods to perform the operations ---------- #
class Trie(object):
    #Init 
    def __init__(self):
        self.root = TrieNode("")
    
    #Method to insert a word
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
    #Method to perform Depth First Search
    def dfs(self, node, prefix):
        if node.is_end:
            self.output.append((prefix + node.char, node.counter))
        for child in node.children.values():
            self.dfs(child, prefix + node.char)
    #Method to query a keyword in the Trie and returning the query results   
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

# ------------------ Creating a trie called dictionary_trie ------------------ #
dictionary_trie = Trie()   

# ----------- Function to insert the dictionary keys into the Trie ----------- #
def insert_main_words():
    for i in dictionary.keys():
        dictionary_trie.insert(i)
    return dictionary_trie

# --- Function to return a set containing recommendations for a given word --- #
def create_recommendations(word):
    word = word.upper()
    rec = set()
    #Recommendations should only be from the dictionary
    if word not in dictionary:
        return rec
    #Read each string from the meaning of the given word
    for me in dictionary[word]:
        for m in me['meanings']:
            #Remove punctuation marks from the string
            temp_string = m.translate(str.maketrans('', '', string.punctuation))
            #Remove digits from the string
            temp_string = temp_string.translate(str.maketrans('', '', string.digits))
            #Seperate each words from the strings
            seperate_words = temp_string.split()
            for sep_word in seperate_words:
                sep_word = sep_word.upper()
                #If seperated word is in our dictionary then append it to recommendations
                if sep_word in dictionary:
                    rec.add(sep_word)
    #Return the set containing recommendations
    return rec

# ------------------------------- Main function ------------------------------ #
def main():
    #Function to read the given dictionary.txt
    read_file()
    #Make dictionary from the merged sentences
    dictionary = make_dictionary(sentences_merged)
    #Insert main words in the Trie
    dictionary_trie = insert_main_words()
    
main()
