"""This module contains the FilesCommandPanel implementation, a class containing a Combobox, a label and three buttons. 

Dependencies:
    tkinter 
    openpyxl: library with writing and reading functionalities of Excel files.
    configparser: library with configuration file reading functionality for exporting Excel files.

Example:
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
from check_values import show_keyboard 

class FilesCommandPanel (tk.Frame): 
    """FilesCommandPanel is a frame containing a Combobox, a label and three buttons.

    Each method related to the FilesManager data structure is associated with a button.

    Attributes:
        files_choice (ttk.Combobox): Combobox with the list of files in FilesManager.
        button_add (tk.Button): button for adding files.
        button_delete (tk.Button): button for deleting files.
        button_export (tk.Button): button for exporting files.
    """

    def __init__(self, master_window: tk.Tk):
        """Initialize ArticlesCommandPanel with master_window.

        Arg:
            master_window (tk.Tk): master application.
        """

        tk.Frame.__init__(self, master = master_window, highlightbackground = 'black', highlightthickness = 2) 

        self.master = master_window

        self._frame_font = 'calibri 20'
        self.relief = 'solid'
        self.borderwidth = 1
        self._padx = 30
        self._pady = 30 

        # Combobox border.
        self.style_combobox = ttk.Style()
        self.style_combobox.theme_use('default')
        self.style_combobox.configure('Custom.TCombobox', relief = 'solid', borderwidth = 3)

        for i in range(5):
            self.rowconfigure(index = i, weight = 1)
             
        self.columnconfigure(index = 0, weight = 1)

        self.label_file = tk.Label(master = self, text = 'File', font = self._frame_font)
        self.label_file.grid(row = 0, column = 0, sticky = 'nswe')

        self.files_choice = ttk.Combobox(master = self, style = 'Custom.TCombobox', values = [], font = self._frame_font)
        self.files_choice.grid(row = 1, column = 0) 
        self.files_choice.bind('<Button-1>', show_keyboard)

        self.button_add = tk.Button(master = self, text = 'Aggiungi File', relief = self.relief, borderwidth = self.borderwidth, font = self._frame_font, command = self.create_file) 
        self.button_add.grid(row = 2, column = 0, sticky = 'nswe', padx = self._padx, pady = self._pady)
        self.button_delete = tk.Button(master = self, text = 'Rimuovi File', relief = self.relief, borderwidth = self.borderwidth, font = self._frame_font, command = self.remove_file) 
        self.button_delete.grid(row = 3, column = 0, sticky = 'nswe', padx = self._padx, pady = self._pady)
        self.button_export = tk.Button(master = self, text = 'Esporta File', relief = self.relief, borderwidth = self.borderwidth, font = self._frame_font, command = self.export_file) 
        self.button_export.grid(row = 4, column = 0, sticky = 'nswe', padx = self._padx, pady = self._pady)

    def create_file(self):
        """Create and add the file specified by the user in the Combobox."""       
        
        file_to_add = self.files_choice.get()

        if file_to_add != '' and file_to_add != ' ':
            ret = self.master.files_manager.insert_file(file_to_add)
            self.files_choice['values'] = self.master.files_manager.get_files()  # Visually refresh the Combobox.

            if ret == True:
                messagebox.showinfo(title = 'Successo!', message = 'File creato con successo.')
            else:
                messagebox.showerror(title = 'Errore!', message = 'File gia\' esistente.')

    def remove_file(self):
        """Delete a file specified by the user in the Combobox."""          
        
        file_to_delete = self.files_choice.get()

        if file_to_delete != '' and file_to_delete != ' ':
            ret = self.master.files_manager.delete_file(file_to_delete)
            self.files_choice['values'] = self.master.files_manager.get_files()  # Visually refresh the Combobox.

            if ret == True:
                 messagebox.showinfo(title = 'Successo!', message = 'File rimosso con successo.')
            else:
                 messagebox.showerror(title = 'Errore!', message = 'File inesistente.')

    def export_file(self):
        """Export a file specified by the user in the Combobox to an Excel file.
        
        In the Excel file, the articles are listed in alphabetical order and the respective quantities in ascending order. 
        
        Use of the openpyxl library for inserting codes as strings in the Excel sheet.
        Example:
            article code: '00010012' 
            if openpyxl is used: '00010012' (str) in Excel
            if openpyxl is not used: '10012' (int) in Excel
        """

        configuration_file = configparser.ConfigParser()
        configuration_file.read('C:\\Users\\Lara\\Desktop\\AppInventario\\AppInventario\\export.ini')
        dest_path = configuration_file['EXPORT']['destination'] 

        file_to_export = self.files_choice.get()

        if file_to_export not in self.master.files_manager.files:
            messagebox.showerror(title = 'Errore!', message = 'File inesistente.')

        else:
            sorted_art = sorted(self.master.files_manager.files[file_to_export].dict_articoli.keys())  # The articles are sorted in alphabetical order.

            sorted_file = {}  # New dictionary where sorted articles are inserted.
            for art in sorted_art:
                sorted_file[art] = self.master.files_manager.files[file_to_export].dict_articoli[art]  # Path indicating the qty list of art in the file_to_export.

            sorted_file = {art: sorted(map(int,qty)) for art, qty in sorted_file.items()}  # Qty are also sorted in ascending order by map() function for conversion to int.

            file_workbook = openpyxl.Workbook()  # A Workbook is created to allow writing to an Excel file.
        
            file_worksheet = file_workbook.active  # Select the active worksheet.

            header = ['Articolo', 'Quantita\'']
            file_worksheet.append(header)

            for art in sorted_file:
                for qty in sorted_file[art]:
                    record = [art, qty]
                    file_worksheet.append(record)

            file_workbook.save(dest_path + file_to_export + '.xlsx')  # Save the Excel file in the specified path. 
        
            messagebox.showinfo(title = 'Successo!', message = 'File esportato con successo.')



