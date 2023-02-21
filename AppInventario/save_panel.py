""" Questo modulo contiene l'implementazione di SavePanel,
una classe che contiene una label e un pulsante.

Dipendenze:
    tkinter 

Esempio:
    from save_panel import SavePanel

    app=tk.Tk() 
    obj=SavePanel(master_window=app) 
    obj.pack() 
    app.mainloop() 
"""
import tkinter as tk 

class SavePanel (tk.Frame): 
    ''' SavePanel e' un frame che contiene una label e un pulsante.

    Attributi:
        button_salva (tk.Button): pulsante con associata funzionalita' di salvataggio di files, articolo e quantita' manipolati
        image (tk.PhotoImage): icona per button_salva
    '''

    def __init__(self, master_window: tk.Tk):
        '''Inizializza SavePanel con master_window

        Argomenti:
            master_window (tk.Tk): applicazione padre
        '''

        tk.Frame.__init__(self, master=master_window, highlightbackground='black', highlightthickness=2) 

        self._frame_font='calibri 20'
        self._padx= 10
        self._pady= 10

        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)

        label_salva=tk.Label(master=self, text='Salva Tutto', font=self._frame_font) 
        label_salva.grid(row=0, column=0, sticky='nswe', padx= self._padx, pady=self._pady)

        self.image=tk.PhotoImage(file='images\save.png')
        self.button_salva=tk.Button(master=self, image=self.image, font=self._frame_font) 
        self.button_salva.grid(row=0, column=1, padx= self._padx, pady=self._pady)

if __name__=='__main__': 
    app=tk.Tk() 
    obj=SavePanel(master_window=app) 
    obj.pack() 
    app.mainloop()
