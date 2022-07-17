# ---------------------------------------------------------------------------- #
#               Graphical User Interface for Webster's dictionary              #
# ---------------------------------------------------------------------------- #

import tkinter as tk
import ctypes
# ---------------------------- Import from main.py --------------------------- #
from main import *


# ----------------------------- Global variables ----------------------------- #
temp_dict = []
#2D list to store the word-recommendations 
temp_rec = []
#Global variable to count the number of word-recommendation windows created 
window_count = 0  
root = tk.Tk()

# ------------ Function to create windows for word-recommendations ----------- #
def create_recommendations_window(word):
    global window_count
    #Set a window ID -> starting from 0
    window_id = window_count
    window_count += 1
    #Creates another window
    window_recommendations = tk.Toplevel(root)
    window_recommendations.geometry("1150x600")
    window_recommendations.title(f"Webster's Dictionary - {word.lower().capitalize()} recommendations")
    word_recommendations_window_label = tk.Label(window_recommendations, text = f"Recommendations for \"{word.lower().capitalize()}\"")
    listbox_recommendations = tk.Listbox(window_recommendations,height= 500, width = 50)
    listbox_recommendations['font'] = "Georgia 15"
    #Creates recommendations from the given word
    recommendations = create_recommendations(word.upper())
    #Appends an empty list to the temp_rec list
    temp_rec.append([])
    l = 0
    for i in recommendations:
        listbox_recommendations.insert(l,i.lower().capitalize())
        l += 1;
        #Insert in the temp_rec list
        temp_rec[window_id].append(i)

    # Function to be triggered when an object is selected from the recommendation list box
    def items_selected(event):
        user_selection = listbox_recommendations.curselection()
        if len(user_selection) != 0:
            selected_word = temp_rec[window_id][user_selection[0]]
            print(selected_word)
            create_window(selected_word)

    word_recommendations_window_label.config(font =("Georgia", 22))
    word_recommendations_window_label.pack(pady=(10,10))
    listbox_recommendations.pack(pady=(20,2))
    #Binding the function items_selected to the event when a selection is made in the listbox
    listbox_recommendations.bind('<<ListboxSelect>>', items_selected) 
    window_recommendations.mainloop()

# ------- Function to create window for word meanings and descriptions ------- #
def create_window(word):
    # To print the selected word and meanings in the console
    print(dictionary[word.upper()])
    #Creates a seperate window for the meanings of each word
    window = tk.Toplevel(root)
    window.title(f"Webster's Dictionary - {word.lower().capitalize()}")
    window.geometry("1150x600")
    word_window_label = tk.Label(window, text = word.lower().capitalize())
    word_window_label.config(font =("Georgia", 30))
    word_window_label.pack(pady=(10,10))
    #Create a label that acts also as a hyper-link to view recommendations for each word
    recommendations_label = tk.Label(window, text = f"See references/recommendations for - {word.lower().capitalize()}", foreground= "blue")
    recommendations_label.config(font =("Georgia", 12,"italic"))
    recommendations_label.pack(pady=(10,10))
    #Binding the function create_recommendations_window to the event when a selection is made in the listbox
    recommendations_label.bind("<Button-1>", lambda e:create_recommendations_window(word))
    #Insert meanings and etymology for each word as a text label
    for i in dictionary[word.upper()]:
        word_et_label = tk.Label(window, text = i['et'],wraplength= 1000)
        word_et_label.config(font =("Georgia", 12 , "italic"))
        word_et_label.pack(pady=(5,30))
        for j in i['meanings']:
            word_meanings_label = tk.Label(window,text= j, wraplength= 1100)
            word_meanings_label.config(font =("Georgia", 12))
            word_meanings_label.pack(pady=(5,15))
    window.mainloop()


def display(): 
    root.title("Webster's Dictionary")
    root.geometry("1080x1080")
    #Increase the DPI of the display window
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  
    root.tk.call('tk', 'scaling', 2)
    #Insert text lables 
    title_label = tk.Label(root, text = "Webster's Dictionary - Search Engine")
    input_description = tk.Label(root, text = "Enter your query here ")
    search_recommendations_label = tk.Label(root, text = "Search Recommendations")

    title_label.config(font =("Georgia", 20))
    input_description.config(font =("Georgia", 13,"bold"))
    search_recommendations_label.config(font =("Georgia", 15,"bold"))

    #Insert search recommendations when user searches for a word
    def label_value():
        j = 0
        listbox.delete(0,tk.END)
        inp = textvar.get().upper()
        del temp_dict[:]
        if inp != '\r' or inp != '\n' or inp != " " or inp != "":
            j = 0
            for i in (dictionary_trie.query(inp)):
                temp_dict.append(i)
            for i in temp_dict:
                listbox.insert(j, i[0].lower().capitalize())
                j += 1

    #Function to create a window for each word with its desciption and etymology
    def items_selected(event):
        user_selection = listbox.curselection()
        if len(user_selection) != 0:
            selected_word = temp_dict[user_selection[0]][0]
            print(selected_word)
            create_window(selected_word)

    textvar = tk.StringVar()
    entry = tk.Entry(root, textvariable=textvar)
    entry['font'] = "Georgia 20"
    entry.focus()
    #Binding the function label_value to the event when user presses enter
    entry.bind("<Return>", lambda x: label_value())

    listbox = tk.Listbox(root,height= 500, width = 50)
    listbox['font'] = "Georgia 15"
    title_label.pack(pady=(20,2))
    input_description.pack(pady=(30,5),padx=(0,200))
    entry.pack(pady=(20,2))
    search_recommendations_label.pack(pady=(30,5))
    listbox.pack(pady=(20,2))
    #Binding the function items_selected to the event when a selection is made in the listbox
    listbox.bind('<<ListboxSelect>>', items_selected)

    tk.mainloop()

display()