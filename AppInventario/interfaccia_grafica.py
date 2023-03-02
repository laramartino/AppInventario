"""Questo modulo contiene l'implementazione di App, una classe che contiene un'interfaccia utente.

Dipendenze:
    tkinter 
    pickle
    FilesCommandPanel: frame che contiene una combobox, tre pulsanti e quattro label.
    ArticlesCommandPanel: frame che contiene quattro pulsanti e quattro label.
    SavePanel: frame che contiene una label e un pulsante.
    FilesManager: struttura dati che rappresenta gli inventari di diverse zone in MP.

Esempio:
    from interfaccia_grafica import App

    obj = App()
    obj.mainloop() 
"""

import tkinter as tk 
import pickle
from files_command_panel import FilesCommandPanel
from articles_command_panel import ArticlesCommandPanel
from save_panel import SavePanel
from files_manager import FilesManager

class App(tk.Tk): 
    """App e' un'interfaccia grafica per un'applicazione di gestione inventari.

    Attributi:
        articles_command_panel (ArticlesCommandPanel): frame che contiene quattro pulsanti e quattro label.
        files_command_panel (FilesCommandPanel): frame che contiene una Combobox, tre pulsanti e quattro label.
        save_panel (SavePanel): frame che contiene una label e un pulsante.
    """

    def __init__(self):
        """Inizializza App."""

        tk.Tk.__init__(self) 
        
        self.files_manager = FilesManager()

        self.title('Barcode Detector') 
        self.geometry('800x800')

        self.rowconfigure(index = 0, weight = 1)
        self.rowconfigure(index = 1, weight = 1)
        self.columnconfigure(index = 0, weight = 1)
        self.columnconfigure(index = 1, weight = 1)

        self.articles_command_panel = ArticlesCommandPanel(master_window = self)
        self.articles_command_panel.grid(row = 0, column = 0, sticky = 'nswe', rowspan = 2)

        self.files_command_panel = FilesCommandPanel(master_window = self) 
        self.files_command_panel.grid(row = 0, column = 1, sticky = 'nswe') 

        self.save_panel = SavePanel(master_window = self)
        self.save_panel.grid(row = 1, column = 1, sticky = 'nswe')

        #Caricamento delle modifiche effettuate dall'ultimo salvataggio dati, grazie all'utilizzo del file binario pickle.
        dati_salvati = open('salvataggio_progressi/dati_salvati.pkl', 'rb') 
        caricamento_dati = pickle.load(dati_salvati)
        self.files_manager.files.update(caricamento_dati)
        dati_salvati.close()

        self.files_command_panel.scelta_files['values'] = [inventario for inventario in caricamento_dati.keys()] #aggiorna visivamente la Combobox.   

if __name__ == '__main__': 
    obj = App()
    obj.mainloop() 