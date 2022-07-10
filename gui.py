import tkinter as tk
import ctypes
# from main import *

def display(): 
    root = tk.Tk()
    root.geometry("1000x1000")
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  

    root.tk.call('tk', 'scaling', 2)

    T = tk.Text(root,height = 1.2,width = 30,font=("Georgia",14))
    l = tk.Label(root, text = "Webster's Dictionary - Search Engine")
    input_description = tk.Label(root, text = "Enter your query here ")
    search_recommendations = tk.Label(root, text = "Search Recommendations")

    l.config(font =("Georgia", 20))
    input_description.config(font =("Georgia", 13,"bold"))
    search_recommendations.config(font =("Georgia", 15,"bold"))
    
    l.pack(pady=(20,2))
    input_description.pack(pady=(30,5),padx=(0,200))
    T.pack()
    search_recommendations.pack(pady=(30,5))
    tk.mainloop()

display()