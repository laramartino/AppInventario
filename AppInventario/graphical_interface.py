"""This module contains the App implementation, a class containing a user interface.

Dependencies:
    tkinter 
    pickle
    FilesCommandPanel: frame containing a Combobox, three buttons and four labels.
    ArticlesCommandPanel: frame containing four buttons, three labels and three entries.
    FilesManager: data structure representing the inventories of different areas in MP.

Example:
    from graphical_interface import App

    obj = App()
    obj.mainloop() 
"""

import tkinter as tk 
import pickle
from files_command_panel import FilesCommandPanel
from articles_command_panel import ArticlesCommandPanel
from files_manager import FilesManager

class App(tk.Tk): 
    """App is a graphical interface for an inventory management application.

    Attributi:
        articles_command_panel (ArticlesCommandPanel): frame containing four buttons, three labels and three entries.
        files_command_panel (FilesCommandPanel): frame containing a Combobox, three buttons and four labels.
    """

    def __init__(self):
        """Initialize App."""

        tk.Tk.__init__(self) 
        
        self.files_manager = FilesManager()

        self.title('Barcode Detector') 
        self.geometry('800x770+0+0') #0+0 the App window appears at the top left of the display.

        self.rowconfigure(index = 0, weight = 1)
        self.columnconfigure(index = 0, weight = 1)
        self.columnconfigure(index = 1, weight = 1)

        self.articles_command_panel = ArticlesCommandPanel(master_window = self)
        self.articles_command_panel.grid(row = 0, column = 0, sticky = 'nswe')

        self.files_command_panel = FilesCommandPanel(master_window = self) 
        self.files_command_panel.grid(row = 0, column = 1, sticky = 'nswe') 

        #Load of the changes made since the last data save, using the pickle binary file.
        saved_data = open('salvataggio_progressi/dati_salvati.pkl', 'rb') 
        loading_data = pickle.load(saved_data)
        self.files_manager.files.update(loading_data)
        saved_data.close()

        self.files_command_panel.scelta_files['values'] = [inventario for inventario in loading_data.keys()] #visually refresh the Combobox. 

        self.protocol("WM_DELETE_WINDOW", self.save_on_close) #when user clicks on the 'X' at the top right of the interface, the save_on_close() function is called.

    def save_on_close(self):
        """Save the changes made since opening the application.

        This function is called when you click on the 'X' at the top right of the interface.
        
        The FilesManager data structure is saved in a pickle binary file.
        """

        saved_data = open('salvataggio_progressi/dati_salvati.pkl', 'wb')
        pickle.dump(self.files_manager.files, saved_data)
        saved_data.close()
        self.destroy() 

if __name__ == '__main__':
    obj = App()
    obj.mainloop() 


