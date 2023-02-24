""" Questo modulo contiene l'implementazione di SavePanel,
una classe che contiene due label e due pulsanti.

Dipendenze:
    tkinter 
    pickle

Esempio:
    from save_panel import SavePanel

    app=tk.Tk() 
    obj=SavePanel(master_window=app) 
    obj.pack() 
    app.mainloop() 
"""

import tkinter as tk 
from tkinter import messagebox
import pickle

class SavePanel (tk.Frame): 
    ''' SavePanel e' un frame che contiene due label e due pulsanti.

    Attributi:
        button_caricamento (tk.Button): pulsante con associata funzionalita' di caricamento dati dall'ultimo salvataggio
        load_image (tk.PhotoImage): icona per button_caricamento
        button_salva (tk.Button): pulsante con associata funzionalita' di salvataggio di files, articolo e quantita' manipolati
        save_image (tk.PhotoImage): icona per button_salva
    '''

    def __init__(self, master_window: tk.Tk):
        '''Inizializza SavePanel con master_window

        Argomenti:
            master_window (tk.Tk): applicazione padre
        '''

        tk.Frame.__init__(self, master=master_window, highlightbackground='black', highlightthickness=2) 

        self.master = master_window

        self._frame_font='calibri 20'
        self._padx= 10
        self._pady= 10

        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)

        label_caricamento=tk.Label(master=self, text='Carica Progressi', font=self._frame_font) 
        label_caricamento.grid(row=0, column=0, sticky='nswe', padx= self._padx, pady=self._pady)
        label_salva=tk.Label(master=self, text='Salva Tutto', font=self._frame_font) 
        label_salva.grid(row=1, column=0, sticky='nswe', padx= self._padx, pady=self._pady)

        self.load_image=tk.PhotoImage(file='images\load.png')
        self.button_caricamento=tk.Button(master=self, image=self.load_image, font=self._frame_font, command=self.carica_dati) 
        self.button_caricamento.grid(row=0, column=1, padx= self._padx, pady=self._pady)
        self.save_image=tk.PhotoImage(file='images\save.png')
        self.button_salva=tk.Button(master=self, image=self.save_image, font=self._frame_font, command=self.salva_dati) 
        self.button_salva.grid(row=1, column=1, padx= self._padx, pady=self._pady)


    def salva_dati(self):
        '''Salva le modifiche effettuate da quando si e' aperta l'applicazione
        
        La struttura dati FilesManager viene salvata in un file binario pickle
        '''

        dati_salvati= open('dati_salvati.pkl', 'wb')
        pickle.dump(self.master.files_manager.files, dati_salvati)
        dati_salvati.close()

        messagebox.showinfo(title='Successo!', message= 'Dati salvati con successo')

    def carica_dati(self):
        '''Carica le modifiche effettuate dall'ultimo salvataggio dati grazie all'utilizzo del file binario pickle'''

        dati_salvati=open('dati_salvati.pkl', 'rb')
        caricamento_dati = pickle.load(dati_salvati)
        self.master.files_manager.files.update(caricamento_dati)

        self.master.files_command_panel.scelta_files['values']=[inventario for inventario in caricamento_dati.keys()] #aggiorna visivamente la Combobox  

        messagebox.showinfo(title='Successo!', message= 'Dati caricati con successo')

