""" Questo modulo contiene l'implementazione di FilesCommandPanel,
una classe che contiene una combobox, tre label e tre pulsanti.

Dipendenze:
    tkinter 

Esempio:
    from files_command_panel import FilesCommandPanel

    app=tk.Tk() 
    obj=FilesCommandPanel(master_window=app) 
    obj.pack() 
    app.mainloop() 
"""

import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox

class FilesCommandPanel (tk.Frame): 
    ''' FilesCommandPanel e' un frame che contiene una combobox, tre label e tre pulsanti.

    Ogni pulsante ha associato un metodo relativo alla struttura dati di FilesManager.

    Attributi:
        scelta_files (ttk.Combobox): combobox con lista di files presenti in FilesManager
        button_aggiungi (tk.Button): pulsante con associata funzionalita' di lettura di aggiunta files
        button_rimuovi (tk.Button): pulsante con associata funzionalita' di rimozione files
        button_esporta (tk.Button): pulsante con associata funzionalita' di esportazione files
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

        for i in range(4):
            self.rowconfigure(index=i, weight=1)

        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)

        self.scelta_files=ttk.Combobox(master=self, values=[], font=self._frame_font)
        self.scelta_files.grid(row=0, column=0, columnspan=2) 

        for i, text in enumerate(['Aggiungi File','Rimuovi File','Esporta File']):
            tk.Label(master=self, text=text, font=self._frame_font).grid(row=i+1, column=0, sticky='nswe')

        
        self.button_aggiungi=tk.Button(master=self, text='Aggiungi', font=self._frame_font, command=self.aggiunta_file) 
        self.button_aggiungi.grid(row=1, column=1, sticky='nswe', padx= self._padx, pady=self._pady)
        self.button_rimuovi=tk.Button(master=self, text='Rimuovi', font=self._frame_font, command=self.elimina_file) 
        self.button_rimuovi.grid(row=2, column=1, sticky='nswe', padx= self._padx, pady=self._pady)
        self.button_esporta=tk.Button(master=self, text='Esporta', font=self._frame_font, command=self.esporta_file) 
        self.button_esporta.grid(row=3, column=1, sticky='nswe', padx= self._padx, pady=self._pady)

    
    def aggiunta_file(self):
        '''Aggiunge un file inserito dall'utente nella Combobox'''          
        
        inserire_file= self.scelta_files.get()

        if inserire_file != '' and inserire_file != ' ':
            ret = self.master.files_manager.inser_file(inserire_file)
            self.scelta_files['values'] = self.master.files_manager.get_files() #aggiorna visivamente Combobox

            if ret==True:
                messagebox.showinfo(title='Successo', message='File creato con successo')
            else:
                messagebox.showerror(title = 'Errore', message='File gia\' esistente')

    def elimina_file(self):
        '''Elimina un file inserito dall'utente nella Combobox'''          
        
        file_da_rimuovere= self.scelta_files.get()

        if file_da_rimuovere != '' and file_da_rimuovere != ' ':
            ret = self.master.files_manager.rimoz_file(file_da_rimuovere)
            self.scelta_files['values'] = self.master.files_manager.get_files() #aggiorna visivamente Combobox

            if ret==True:
                messagebox.showinfo(title='Successo', message='File rimosso con successo')
            else:
                messagebox.showerror(title = 'Errore', message='File inesistente')

    def esporta_file(self):
        '''Esporta un file indicato dall'utente nella Combobox

        self.master indica il Tk
        files_manager.files indica il dizionario di FilesManager
        [file_da_esportare] indica il file da esportare dentro FilesManager
        dict_articoli indica il dizionario degli articoli in ArticlesManager del file da esportare
        [articolo] indica la lista delle quantita' degli articoli da esportare
        '''

        file_da_esportare=self.scelta_files.get()

        file_csv= open(file_da_esportare+'.csv', 'w')
        file_csv.write("Articolo;Quantita';")

        for articolo in self.master.files_manager.files[file_da_esportare].dict_articoli: 
            for qty in self.master.files_manager.files[file_da_esportare].dict_articoli[articolo]:
                file_csv.write('\n'+articolo+';'+qty)

        file_csv.close()
        
        messagebox.showinfo(title='Successo', message='File esportato con successo')

if __name__=='__main__': 
    app=tk.Tk() 
    obj=FilesCommandPanel(master_window=app) 
    obj.pack() 
    app.mainloop()
