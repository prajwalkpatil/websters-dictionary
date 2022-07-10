import tkinter as tk
import ctypes
from main import *

temp_dict = []

def create_window(word):
    print(dictionary[word.upper()])

def display(): 
    root = tk.Tk()
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
            # window = tk.Toplevel(root)



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