""" Questo modulo contiene l'implementazione di ArticlesCommandPanel,
una classe che contiene quattro label e quattro pulsanti.

Dipendenze:
    tkinter 

Esempio:
    from frame1 import ArticlesCommandPanel

    app=tk.Tk() 
    obj=ArticlesCommandPanel(master_window=app) 
    obj.pack() 
    app.mainloop() 
"""

import tkinter as tk 
from check_valori import check_art, check_qty
from tkinter import messagebox
from video_detection import video_detection

class ArticlesCommandPanel (tk.Frame): 
    ''' ArticlesCommandPanel e' un frame che contiene quattro label e quattro pulsanti.

    Ogni pulsante ha associato un metodo relativo alla struttura dati di ArticlesManager.

    Attributi:
        button_avvia (tk.Button): pulsante con associata funzionalita' di lettura di QRcodes/barcodes
        button_insert (tk.Button): pulsante con associata funzionalita' di inserimento files
        button_modifica (tk.Button): pulsante con associata funzionalita' di modifica files
        button_cancella (tk.Button): pulsante con associata funzionalita' di rimozione files
    '''

    def __init__(self, master_window: tk.Tk):
        '''Inizializza ArticlesCommandPanel con master_window

        Argomenti:
            master_window (tk.Tk): applicazione padre
        '''

        tk.Frame.__init__(self, master=master_window, highlightbackground='black', highlightthickness=2) 

        self.master = master_window

        self._frame_font='calibri 20'
        self._padx= 10
        self._pady= 30 

        for i in range(7):
            self.rowconfigure(index=i, weight=1)

        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)

        for i, text in enumerate(['Avvia Lettura','Articolo', 'Qty', 'Inserisci', 'Cancella', 'Modifica', 'Qty da\nAggiornare']):
            tk.Label(master=self, text=text, font=self._frame_font).grid(row=i, column=0, sticky='nswe')

        self.button_avvia=tk.Button(master=self, text='Avvia Lettura', font=self._frame_font, command=video_detection)
        self.button_avvia.grid(row=0, column=1, sticky='nswe', padx= self._padx, pady=self._pady)
        self.entry_art= tk.Entry(master=self, font=self._frame_font)
        self.entry_art.grid(row=1, column=1, sticky='nswe', padx= self._padx, pady=self._pady)
        self.entry_qty_nuova= tk.Entry(master=self, font=self._frame_font)
        self.entry_qty_nuova.grid(row=2, column=1, sticky='nswe', padx= self._padx, pady=self._pady)
        self.button_insert=tk.Button(master=self, text='Inserisci', font=self._frame_font, command=self.aggiunta_art) 
        self.button_insert.grid(row=3, column=1, sticky='nswe', padx= self._padx, pady=self._pady)
        self.button_cancella=tk.Button(master=self, text='Cancella', font=self._frame_font, command= self.elimina_qty) 
        self.button_cancella.grid(row=4, column=1, sticky='nswe', padx= self._padx, pady=self._pady)
        self.button_modifica=tk.Button(master=self, text='Modifica', font=self._frame_font, command= self.modifica_qty) 
        self.button_modifica.grid(row=5, column=1, sticky='nswe', padx= self._padx, pady=self._pady)
        self.entry_qty_vecchia= tk.Entry(master=self, font=self._frame_font)
        self.entry_qty_vecchia.grid(row=6, column=1, sticky='nswe', padx= self._padx, pady=self._pady)

    def aggiunta_art(self):
        '''Aggiunge una coppia articolo-quantita' nuova inserito dall'utente nelle entries'''

        file_inserito= self.master.files_command_panel.scelta_files.get()  #controllare che non sia null 
        articolo=self.entry_art.get()
        qty=self.entry_qty_nuova.get()

        if file_inserito not in self.master.files_manager.files:
            messagebox.showerror(title = 'Errore', message='File invalido.')
            return 

        if check_art(articolo) == False:
            messagebox.showerror(title = 'Errore', message='Articolo non valido.')
            return 

        if check_qty(qty) == False:
            messagebox.showerror(title = 'Errore', message="Quantita' non valida.")
            return
        
        ret = self.master.files_manager.files[file_inserito].inser_val((articolo,qty))
        messagebox.showinfo(title='Successo', message='Record inserito con successo.')

        print(self.master.files_manager.files)

    def elimina_qty(self):
        '''Elimina una quantita' presente in ArticlesManager inserita dall'utente, 
        indicando l'articolo corrispondente'''   
        
        file_inserito= self.master.files_command_panel.scelta_files.get()  #controllare che non sia null 
        articolo=self.entry_art.get()
        qty=self.entry_qty_nuova.get()

        if file_inserito not in self.master.files_manager.files:
            messagebox.showerror(title = 'Errore', message='File invalido.')
            return 

        if check_art(articolo) == False:
            messagebox.showerror(title = 'Errore', message='Articolo non valido.')
            return 

        if check_qty(qty) == False:
            messagebox.showerror(title = 'Errore', message="Quantita' non valida.")
            return
        
        ret = self.master.files_manager.files[file_inserito].rimoz_val((articolo,qty))
        if ret==True:
            messagebox.showinfo(title='Successo', message='Record rimosso con successo.')
        else:
            messagebox.showerror(title='Errore', message='Record invalido.')

    def modifica_qty(self):
        '''Modifica una quantita' di un articolo presente in ArticlesManager inserita dall'utente, 
        indicando l'articolo e la quantita' precedente corrispondente'''   
        
        file_inserito= self.master.files_command_panel.scelta_files.get()  #controllare che non sia null 
        articolo=self.entry_art.get()
        new_qty=self.entry_qty_nuova.get()
        old_qty=self.entry_qty_vecchia.get()

        if file_inserito not in self.master.files_manager.files:
            messagebox.showerror(title = 'Errore', message='File invalido.')
            return 

        if check_art(articolo) == False:
            messagebox.showerror(title = 'Errore', message='Articolo non valido.')
            return 

        if check_qty(new_qty) == False:
            messagebox.showerror(title = 'Errore', message="Quantita' non valida.")
            return

        if old_qty not in self.master.files_manager.files[file_inserito].dict_articoli[articolo]:
            messagebox.showerror(title = 'Errore', message="Quantita' non presente per l'articolo "+ articolo) 
            return

        if check_qty(old_qty) == False:
            messagebox.showerror(title = 'Errore', message="Quantita' non valida.")
            return
        
        ret = self.master.files_manager.files[file_inserito].modifica_val((articolo,old_qty, new_qty))
        if ret==True:
            messagebox.showinfo(title='Successo', message='Record modificato con successo.')
        else:
            messagebox.showerror(title='Errore', message='Record invalido.')

if __name__=='__main__': 
    app=tk.Tk() 
    obj=ArticlesCommandPanel(master_window=app) 
    obj.pack() 
    app.mainloop() 