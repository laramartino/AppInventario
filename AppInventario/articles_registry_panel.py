"""This module contains the ArticlesRegistryPanel implementation, a class containing an entry and a button. 

Dependencies:
    tkinter 
    check_values: the module containing the implementation of functions that check the values of article, new article and quantity inserted by user.
    pandas: library for manipulating data in Excel files. 
    openpyxl: library with writing and reading functionalities of Excel files.

Example:
    from articles_registry_panel import ArticlesRegistryPanel

    app = tk.Tk() 
    obj = ArticlesRegistryPanel(master_window = app) 
    obj.pack() 
    app.mainloop() 
"""

import tkinter as tk 
from tkinter import messagebox
from check_values import *
import pandas as pd
import openpyxl 

class ArticlesRegistryPanel (tk.Frame): 
    """ArticlesRegistryPanel is a frame containing an entry and a button.

    Attributes: 
        button_add (tk.Button): button for adding a new article to the MP registry.
    """

    def __init__(self, master_window: tk.Tk):
        """Initialize ArticlesRegistryPanel with master_window.

        Arg:
            master_window (tk.Tk): master application.
        """

        tk.Frame.__init__(self, master = master_window, highlightbackground = 'black', highlightthickness = 2) 

        self.master = master_window

        self._frame_font = 'calibri 20'
        self.relief = 'solid'
        self.borderwidth = 1
        self._padx = 35
        self._pady = 30 
        
        self.rowconfigure(index = 0, weight = 1)
        self.rowconfigure(index = 1, weight = 1)
        self.columnconfigure(index = 0, weight = 1)

        self.entry_new_art = tk.Entry(master = self, relief = self.relief, borderwidth = self.borderwidth, font = self._frame_font)
        self.entry_new_art.grid(row = 0, column = 0, sticky = 'nswe', padx = self._padx, pady = self._pady)
        self.entry_new_art.bind('<Button-1>', show_keyboard)
        self.button_add = tk.Button(master = self, text = 'Aggiungi Articolo\nin Anagrafica', relief = self.relief, borderwidth = self.borderwidth, font = self._frame_font, command = self.add_article) 
        self.button_add.grid(row = 1, column = 0, sticky = 'nswe', padx = self._padx, pady = self._pady)

    def add_article(self):
        """Add the article specified by the user in the entry to the MP registry (Excel file)."""       
        
        article_to_add = self.entry_new_art.get()
        ret = check_new_art(article_to_add)

        if ret == True:

            #Read Excel file and get the 'ARTICOLO' column as a list of str.
            articles_mp_list = pd.read_excel('C:\\Users\\Lara\\source\\repos\\laramartino\\AppInventario\\AppInventario\\anagrafica_articoli.xlsx')['ARTICOLO'].tolist() 
            articles_mp_list.append(article_to_add)
            articles_mp_list.sort()

            file_workbook = openpyxl.Workbook() #A Workbook is created to allow writing to an Excel file.
            file_worksheet = file_workbook.active #Select the active worksheet.

            header = ['ARTICOLO']
            file_worksheet.append(header)
            for art in articles_mp_list:    
                file_worksheet.append([art])
            file_workbook.save('C:\\Users\\Lara\\source\\repos\\laramartino\\AppInventario\\AppInventario\\anagrafica_articoli.xlsx') 
            
            messagebox.showinfo(title = 'Successo!', message = 'Articolo aggiunto correttamente.')
        
        else:
            messagebox.showerror(title = 'Errore!', message = 'Articolo gia\' presente o invalido.')







