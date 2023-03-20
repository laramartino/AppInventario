"""This module contains ArticlesCommandPanel implementation, a class containing three labels, four buttons and three entries.

Dependencies:
    tkinter 
    check_valori: the module containing the implementation of functions that check the values of article and quantity inserted by user. 
    video_detection: the module containing VideoDetection implementation.

Example:
    from articles_command_panel import ArticlesCommandPanel

    app = tk.Tk() 
    obj = ArticlesCommandPanel(master_window = app) 
    obj.pack() 
    app.mainloop() 
"""

import tkinter as tk 
from tkinter import messagebox
from check_values import *
from video_detection import VideoDetection 

class ArticlesCommandPanel (tk.Frame): 
    """ArticlesCommandPanel is a frame containing three labels, four buttons and three entries.

    Each method related to the ArticlesManager data structure is associated with a button.

    Attributes:
        button_detection (tk.Button): button for detecting and decoding barcodes.
        button_insert (tk.Button): button for adding records.
        button_modify (tk.Button): button for modifying a quantity of an article.
        button_delete (tk.Button): button for deleting a quantity of an article.
    """

    def __init__(self, master_window: tk.Tk):
        """Initialize ArticlesCommandPanel with master_window.

        Arg:
            master_window (tk.Tk): master application.
        """

        tk.Frame.__init__(self, master = master_window, highlightbackground = 'black', highlightthickness = 2) 

        self.master = master_window
        self.video_detection = VideoDetection(master_window = self) 

        self._frame_font = 'calibri 20'
        self.relief = 'solid'
        self.borderwidth = 1
        self._padx = 30
        self._pady = 30 

        for i in range(7):
            self.rowconfigure(index = i, weight = 1)

        self.columnconfigure(index = 0, weight = 1)
        self.columnconfigure(index = 1, weight = 1)

        tk.Label(master = self, text = 'Articolo', font = self._frame_font).grid(row = 1, column = 0, sticky = 'nswe')
        tk.Label(master = self, text = 'Qty', font = self._frame_font).grid(row = 2, column = 0, sticky = 'nswe')
        tk.Label(master = self, text = 'Qty da\nAggiornare', font = self._frame_font).grid(row = 6, column = 0, sticky = 'nswe')

        self.button_detection = tk.Button(master = self, text = 'Avvia Lettura', relief = self.relief, borderwidth = self.borderwidth, font = self._frame_font, command = self.video_detection.video_detection)
        self.button_detection.grid(row = 0, column = 0, sticky = 'nswe', columnspan = 2, padx = self._padx, pady = self._pady)
        self.entry_art = tk.Entry(master = self, relief = self.relief, borderwidth = self.borderwidth, font = self._frame_font)
        self.entry_art.grid(row = 1, column = 1, sticky = 'nswe', padx = self._padx, pady = self._pady)
        self.entry_new_qty = tk.Entry(master = self, relief = self.relief, borderwidth = self.borderwidth, font = self._frame_font)
        self.entry_new_qty.grid(row = 2, column = 1, sticky = 'nswe', padx = self._padx, pady = self._pady)
        self.button_insert = tk.Button(master = self, text = 'Inserisci', relief = self.relief, borderwidth = self.borderwidth, font = self._frame_font, command = self.insert_art_qty) 
        self.button_insert.grid(row = 3, column = 0, sticky = 'nswe', columnspan = 2, padx = self._padx, pady = self._pady)
        self.button_delete = tk.Button(master = self, text = 'Cancella', relief = self.relief, borderwidth = self.borderwidth, font = self._frame_font, command = self.remove_qty) 
        self.button_delete.grid(row = 4, column = 0, sticky = 'nswe', columnspan = 2, padx = self._padx, pady = self._pady)
        self.button_modify = tk.Button(master = self, text = 'Modifica', relief = self.relief, borderwidth = self.borderwidth, font = self._frame_font, command = self.modify_qty) 
        self.button_modify.grid(row = 5, column = 0, sticky = 'nswe', columnspan = 2, padx = self._padx, pady = self._pady)
        self.entry_old_qty = tk.Entry(master = self, relief = self.relief, borderwidth = self.borderwidth, font = self._frame_font)
        self.entry_old_qty.grid(row = 6, column = 1, sticky = 'nswe', padx = self._padx, pady = self._pady)

    def insert_art_qty(self):
        """Add a new record article-quantity specified by the user to ArticlesManager."""

        inserted_file = self.master.files_command_panel.scelta_files.get()  
        article = self.entry_art.get()
        qty = self.entry_new_qty.get()

        if inserted_file not in self.master.files_manager.files:
            messagebox.showerror(title = 'Errore!', message = 'File inesistente.')
            return 

        if check_art(article) == False:
            messagebox.showerror(title = 'Errore!', message = 'Articolo non valido.')
            return 

        if check_qty(qty) == False:
            messagebox.showerror(title = 'Errore!', message = 'Quantita\' non valida.')
            return
        
        self.master.files_manager.files[inserted_file].insert_record((article, qty))
        messagebox.showinfo(title = 'Successo!', message = 'Record inserito con successo.')

    def remove_qty(self):
        """Delete a quantity of an article specified by the user from ArticlesManager."""
        
        inserted_file = self.master.files_command_panel.scelta_files.get()  
        article = self.entry_art.get()
        qty = self.entry_new_qty.get()

        if inserted_file not in self.master.files_manager.files:
            messagebox.showerror(title = 'Errore!', message = 'File inesistente.')
            return 

        if check_art(article) == False:
            messagebox.showerror(title = 'Errore!', message = 'Articolo non valido.')
            return 

        if check_qty(qty) == False:
            messagebox.showerror(title = 'Errore!', message = 'Quantita\' non valida.')
            return
        
        ret = self.master.files_manager.files[inserted_file].delete_qty((article, qty))
        if ret == True:
            messagebox.showinfo(title = 'Successo!', message = 'Quantita\' rimossa con successo per l\'articolo ' + article)
        else:
            messagebox.showerror(title = 'Errore!', message = 'Record invalido.')

    def modify_qty(self):
        """Modify a quantity of an article in ArticlesManager, the user specifies the article and the old quantity."""  
        
        inserted_file = self.master.files_command_panel.scelta_files.get()  
        article = self.entry_art.get()
        new_qty = self.entry_new_qty.get()
        old_qty = self.entry_old_qty.get()

        if inserted_file not in self.master.files_manager.files:
            messagebox.showerror(title = 'Errore!', message = 'File non esistente.')
            return 

        if check_art(article) == False:
            messagebox.showerror(title = 'Errore!', message = 'Articolo non valido.')
            return 

        if check_qty(new_qty) == False:
            messagebox.showerror(title = 'Errore!', message = 'Quantita\' non valida.')
            return

        if old_qty not in self.master.files_manager.files[inserted_file].dict_articoli[article]:
            messagebox.showerror(title = 'Errore!', message = 'Quantita\' non presente per l\'articolo ' + article) 
            return

        if check_qty(old_qty) == False:
            messagebox.showerror(title = 'Errore!', message = 'Quantita\' da aggiornare non valida.')
            return
        
        ret = self.master.files_manager.files[inserted_file].modify_record((article, old_qty, new_qty))
        if ret == True:
            messagebox.showinfo(title = 'Successo!', message = 'Quantita\' modificata con successo per l\'articolo ' + article)
        else:
            messagebox.showerror(title = 'Errore!', message = 'Record invalido.')



