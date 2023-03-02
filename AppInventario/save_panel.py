"""Questo modulo contiene l'implementazione di SavePanel,
una classe che contiene una label e un pulsante.

Dipendenze:
    tkinter 
    pickle

Esempio:
    from save_panel import SavePanel

    app = tk.Tk() 
    obj=SavePanel(master_window = app) 
    obj.pack() 
    app.mainloop() 
"""

import tkinter as tk 
from tkinter import messagebox
import pickle

class SavePanel (tk.Frame): 
    """SavePanel e' un frame che contiene una label e un pulsante.

    Attributi:
        button_salva (tk.Button): pulsante con associata funzionalita' di salvataggio files, articoli e quantita' manipolati.
        save_image (tk.PhotoImage): icona per button_salva.
    """

    def __init__(self, master_window: tk.Tk):
        """Inizializza SavePanel con master_window.

        Argomenti:
            master_window (tk.Tk): applicazione padre.
        """

        tk.Frame.__init__(self, master=master_window, highlightbackground='black', highlightthickness=2) 

        self.master = master_window

        self._frame_font = 'calibri 20'
        self._padx = 10
        self._pady = 10

        self.rowconfigure(index = 0, weight = 1)
        self.columnconfigure(index = 0, weight = 1)
        self.columnconfigure(index = 1, weight = 1)

        label_salva = tk.Label(master = self, text = 'Salva Tutto', font = self._frame_font) 
        label_salva.grid(row = 0, column = 0, sticky = 'nswe', padx = self._padx, pady = self._pady)

        self.save_image = tk.PhotoImage(file = 'images\save.png')
        self.button_salva = tk.Button(master = self, image = self.save_image, font = self._frame_font, command = self.salva_dati) 
        self.button_salva.grid(row = 0, column = 1, padx = self._padx, pady = self._pady)


    def salva_dati(self):
        """Salva le modifiche effettuate da quando si e' aperta l'applicazione.
        
        La struttura dati FilesManager viene salvata in un file binario pickle.
        """

        dati_salvati = open('salvataggio_progressi/dati_salvati.pkl', 'wb')
        pickle.dump(self.master.files_manager.files, dati_salvati)
        dati_salvati.close()

        messagebox.showinfo(title = 'Successo!', message = 'Dati salvati con successo.')
