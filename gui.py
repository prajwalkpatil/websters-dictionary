import tkinter as tk
import ctypes
from main import *

temp_dict = []
temp_rec = []
root = tk.Tk()

def create_recommendations_window(word):
    window_recommendations = tk.Toplevel(root)
    window_recommendations.geometry("1150x600")
    window_recommendations.title(f"Webster's Dictionary - {word.lower().capitalize()} recommendations")
    word_recommendations_window_label = tk.Label(window_recommendations, text = f"Recommendations for \"{word.lower().capitalize()}\"")

    listbox_recommendations = tk.Listbox(window_recommendations,height= 500, width = 50)
    listbox_recommendations['font'] = "Georgia 15"
    recommendations = create_recommendations(word.upper())
    del temp_rec[:]
    l = 0
    for i in recommendations:
        listbox_recommendations.insert(l,i.lower().capitalize())
        l += 1;
        temp_rec.append(i)

    def items_selected(event):
        user_selection = listbox_recommendations.curselection()
        if len(user_selection) != 0:
            selected_word = temp_rec[user_selection[0]]
            print(selected_word)
            create_window(selected_word)

    word_recommendations_window_label.config(font =("Georgia", 22))
    word_recommendations_window_label.pack(pady=(10,10))
    listbox_recommendations.pack(pady=(20,2))
    listbox_recommendations.bind('<<ListboxSelect>>', items_selected) 
    window_recommendations.mainloop()

def create_window(word):
    print(dictionary[word.upper()])
    window = tk.Toplevel(root)
    window.title(f"Webster's Dictionary - {word.lower().capitalize()}")
    window.geometry("1150x600")
    word_window_label = tk.Label(window, text = word.lower().capitalize())
    word_window_label.config(font =("Georgia", 30))
    word_window_label.pack(pady=(10,10))
    recommendations_label = tk.Label(window, text = f"See references/recommendations for - {word.lower().capitalize()}", foreground= "blue")
    recommendations_label.config(font =("Georgia", 12,"italic"))
    recommendations_label.pack(pady=(10,10))
    recommendations_label.bind("<Button-1>", lambda e:create_recommendations_window(word))

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
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  

    root.tk.call('tk', 'scaling', 2)

    title_label = tk.Label(root, text = "Webster's Dictionary - Search Engine")
    input_description = tk.Label(root, text = "Enter your query here ")
    search_recommendations_label = tk.Label(root, text = "Search Recommendations")

    title_label.config(font =("Georgia", 20))
    input_description.config(font =("Georgia", 13,"bold"))
    search_recommendations_label.config(font =("Georgia", 15,"bold"))

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
                # print(i[0].lower().capitalize())

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
    
    entry.bind("<Return>", lambda x: label_value())
    
    listbox = tk.Listbox(root,height= 500, width = 50)
    listbox['font'] = "Georgia 15"
    title_label.pack(pady=(20,2))
    input_description.pack(pady=(30,5),padx=(0,200))
    entry.pack(pady=(20,2))
    search_recommendations_label.pack(pady=(30,5))
    listbox.pack(pady=(20,2))
    listbox.bind('<<ListboxSelect>>', items_selected)

    tk.mainloop()

display()