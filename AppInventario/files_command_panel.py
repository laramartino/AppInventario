""" Questo modulo contiene l'implementazione di FilesCommandPanel,
una classe che contiene una combobox, una label e tre pulsanti.

Dipendenze:
    tkinter 
    openpyxl: libreria con funzionalita' di scrittura e lettura di file Excel
    configparser: libreria utile alla lettura di file di configurazione per l'esportazione dei file Excel

Esempio:
    from files_command_panel import FilesCommandPanel

    app = tk.Tk() 
    obj = FilesCommandPanel(master_window = app) 
    obj.pack() 
    app.mainloop() 
"""

import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox
import openpyxl
import configparser

class FilesCommandPanel (tk.Frame): 
    """FilesCommandPanel e' un frame che contiene una combobox, una label e tre pulsanti.

    Ogni pulsante ha associato un metodo relativo alla struttura dati di FilesManager.

    Attributi:
        scelta_files (ttk.Combobox): combobox con lista di files presenti in FilesManager.
        button_aggiungi (tk.Button): pulsante con associata funzionalita' di aggiunta files.
        button_rimuovi (tk.Button): pulsante con associata funzionalita' di rimozione files.
        button_esporta (tk.Button): pulsante con associata funzionalita' di esportazione files.
    """

    def __init__(self, master_window: tk.Tk):
        """Inizializza ArticlesCommandPanel con master_window.

        Argomenti:
            master_window (tk.Tk): applicazione padre.
        """

        tk.Frame.__init__(self, master = master_window, highlightbackground = 'black', highlightthickness = 2) 

        self.master = master_window

        self._frame_font ='calibri 20'
        self.relief = 'solid'
        self.borderwidth = 1
        self._padx = 20
        self._pady = 70 

        #bordi per Combobox
        self.style_combobox = ttk.Style()
        self.style_combobox.theme_use('default')
        self.style_combobox.configure('Custom.TCombobox', relief = 'solid', borderwidth = 3)

        for i in range(5):
            self.rowconfigure(index = i, weight = 1)
             
        self.columnconfigure(index = 0, weight = 1)

        self.label_file = tk.Label(master = self, text = 'File', font = self._frame_font)
        self.label_file.grid(row = 0, column = 0, sticky = 's')

        self.scelta_files = ttk.Combobox(master = self, style = 'Custom.TCombobox', values = [], font = self._frame_font)
        self.scelta_files.grid(row = 1, column = 0) 

        self.button_aggiungi = tk.Button(master = self, text = 'Aggiungi File', relief = self.relief, borderwidth = self.borderwidth, font = self._frame_font, command = self.create_file) 
        self.button_aggiungi.grid(row = 2, column = 0, sticky = 'nswe', padx = self._padx, pady = self._pady)
        self.button_rimuovi = tk.Button(master = self, text = 'Rimuovi File', relief = self.relief, borderwidth = self.borderwidth, font = self._frame_font, command = self.remove_file) 
        self.button_rimuovi.grid(row = 3, column = 0, sticky = 'nswe', padx = self._padx, pady = self._pady)
        self.button_esporta = tk.Button(master = self, text = 'Esporta File', relief = self.relief, borderwidth = self.borderwidth, font = self._frame_font, command = self.export_file) 
        self.button_esporta.grid(row = 4, column = 0, sticky = 'nswe', padx = self._padx, pady = self._pady)

    def create_file(self):
        """Crea e aggiunge un file inserito dall'utente nella Combobox"""       
        
        file_da_aggiungere = self.scelta_files.get()

        if file_da_aggiungere != '' and file_da_aggiungere != ' ':
            ret = self.master.files_manager.insert_file(file_da_aggiungere)
            self.scelta_files['values'] = self.master.files_manager.get_files() #aggiorna visivamente Combobox.

            if ret == True:
                messagebox.showinfo(title = 'Successo!', message = 'File creato con successo.')
            else:
                messagebox.showerror(title = 'Errore!', message = 'File gia\' esistente.')

    def remove_file(self):
        """Elimina un file inserito dall'utente nella Combobox"""          
        
        file_da_rimuovere = self.scelta_files.get()

        if file_da_rimuovere != '' and file_da_rimuovere != ' ':
            ret = self.master.files_manager.delete_file(file_da_rimuovere)
            self.scelta_files['values'] = self.master.files_manager.get_files() #aggiorna visivamente Combobox.

            if ret == True:
                 messagebox.showinfo(title = 'Successo!', message = 'File rimosso con successo.')
            else:
                 messagebox.showerror(title = 'Errore!', message = 'File inesistente.')

    def export_file(self):
        """Esporta un file indicato dall'utente nella Combobox in un file Excel, 
        in cui gli articoli sono elencati in ordine alfabetico e le rispettive quantita' in ordine crescente.
        
        Uso della libreria openpyxl per l'inserimento dei codici come stringhe nel foglio Excel.
        Esempio:
            codice articolo: '00010012' 
            con utilizzo di openpyxl: '00010012' (str) in Excel
            senza utilizzo di openpyxl: '10012' (int) in Excel
        """

        configuration_file = configparser.ConfigParser()
        configuration_file.read('export.ini')
        dest_path = configuration_file['EXPORT']['destination'] 

        file_da_esportare = self.scelta_files.get()

        if file_da_esportare not in self.master.files_manager.files:
            messagebox.showerror(title = 'Errore!', message = 'File inesistente.')

        else:
            sorted_art = sorted(self.master.files_manager.files[file_da_esportare].dict_articoli.keys()) #articoli in ordine alfabetico.

            sorted_file = {} #nuovo dizionario in cui inserire gli articoli ordinati.
            for art in sorted_art:
                sorted_file[art] = self.master.files_manager.files[file_da_esportare].dict_articoli[art] #percorso che indica la lista delle qty di art nel file_da_esportare.

            sorted_file = {art: sorted(map(int,qty)) for art, qty in sorted_file.items()} #anche qty in ordine crescente con funzione map() per conversione in int.

            file_workbook = openpyxl.Workbook() #crea un Workbook che permette la scrittura su un file Excel.
        
            file_worksheet = file_workbook.active #seleziona il worksheet attivo.

            header = ['Articolo', 'Quantita\'']
            file_worksheet.append(header)

            for art in sorted_file:
                for qty in sorted_file[art]:
                    record = [art, qty]
                    file_worksheet.append(record)

            file_workbook.save(dest_path + '/files/' + file_da_esportare + '.xlsx') #salva il file Excel nel percorso indicato. 
        
            messagebox.showinfo(title = 'Successo!', message = 'File esportato con successo.')

