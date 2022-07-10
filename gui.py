import tkinter as tk
import ctypes
from main import *

def callback(*args):
    print("value changed!")


def display(): 
    root = tk.Tk()
    root.geometry("1000x1000")
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  

    root.tk.call('tk', 'scaling', 2)

    title_label = tk.Label(root, text = "Webster's Dictionary - Search Engine")
    input_description = tk.Label(root, text = "Enter your query here ")
    search_recommendations_label = tk.Label(root, text = "Search Recommendations")

    title_label.config(font =("Georgia", 20))
    input_description.config(font =("Georgia", 13,"bold"))
    search_recommendations_label.config(font =("Georgia", 15,"bold"))

    def label_value():
        listbox.insert(tk.END, textvar.get())
        print(textvar.get())

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

    tk.mainloop()

display()