"""Questo modulo contiene l'implementazione di VideoDetection,
una classe contenente quattro metodi relativi alla decodifica di barcodes
e all'inserimento delle informazioni rilevate nelle struttura dati FilesManager e ArticlesManager.

Dipendenze:
    cv2 (OpenCV): libreria riguardo la visione artificiale in tempo reale.
    pyzbar: libreria di supporto a cv2.
    tkinter
    check_valori: modulo contenente l'implementazione di funzioni che controllano i valori di articolo e quantita' rilevati.
"""

import cv2
from pyzbar import pyzbar
from check_valori import *
import tkinter as tk
from tkinter import messagebox 

class VideoDetection:
    """VideoDetection e' una classe con quattro metodi relativi alla decodifica di barcodes
    e all'inserimento delle informazioni rilevate nelle strutture dati FilesManager e ArticlesManager.

    Attributi:
        entry_art (None): nei metodi diventa una entry per la manipolazione dell'articolo rilevato.
        entry_qty (None): nei metodi diventa una entry per la manipolazione della quantita' rilevata.
        popup (None): nei metodi diventa un tk.Toplevel.
    """

    def __init__(self, master_window: tk.Tk):
        """Inizializza VideoDetection con master_window.

        Argomenti:
            master_window (tk.Tk): applicazione padre.
        """

        self.vd_master = master_window 
        self.entry_art = None 
        self.entry_qty = None
        self.popup = None

    def show_popup(self, decoded_text_list: list):
        """Quando vengono rilevati i barcodes, 
        viene mostrato un tk.Toplevel con due entries e due button.

        Arg:
            decoded_text (list): lista contenente articolo e quantita' da inserire.
        """

        popup_window = True

        if check_art(decoded_text_list[0]) == True and check_qty(decoded_text_list[1]) == True:
            art = decoded_text_list[0]
            qty = decoded_text_list[1]
        elif check_art(decoded_text_list[1]) == True and check_qty(decoded_text_list[0]) == True:
            qty = decoded_text_list[0]
            art = decoded_text_list[1]
        else:
            messagebox.showerror(title = 'Errore!', message = 'Articolo e\o quantita\' non validi.')
            popup_window = False #non appare il popup

        if popup_window: #if popup_window == True
            self.popup = tk.Toplevel()
            self.popup.title('Codici rilevati')

            #dimensioni della finestra dello schermo
            screen_width = self.popup.winfo_screenwidth()
            screen_height = self.popup.winfo_screenheight()

            #dimensioni della finestra popup
            popup_width = 600
            popup_height = 300

            #posizione x, y della finestra popup
            x = int((screen_width / 2) - (popup_width / 2))
            y = int((screen_height / 2) - (popup_height / 2))

            #finestra popup al centro dello schermo
            self.popup.geometry('{}x{}+{}+{}'.format(popup_width, popup_height, x, y))

            font = 'calibri 20'
            padx = 10
            pady = 30

            self.popup.rowconfigure(index = 0, weight = 1)
            self.popup.rowconfigure(index = 1, weight = 1)
            self.popup.rowconfigure(index = 2, weight = 1)
            self.popup.columnconfigure(index = 0, weight = 1)
            self.popup.columnconfigure(index = 1, weight = 1)

            label_articolo = tk.Label(self.popup, text = 'Articolo: ', font = font)
            label_articolo.grid(row = 0, column = 0, sticky = 'nswe')
            self.entry_art = tk.Entry(self.popup, font = font)
            self.entry_art.grid(row = 0, column = 1, sticky = 'nswe', padx = padx, pady = pady)
            self.entry_art.insert(0, art)
            label_quantita = tk.Label(self.popup, text = 'Qty: ', font = font)
            label_quantita.grid(row = 1, column = 0, sticky = 'nswe')
            self.entry_qty = tk.Entry(self.popup, font = font)
            self.entry_qty.grid(row = 1, column = 1, sticky = 'nswe', padx = padx, pady = pady)
            self.entry_qty.insert(0, qty)

            button_aggiungi = tk.Button(self.popup, text = 'Aggiungi', font = font, command = self.insert_video_record)
            button_aggiungi.grid(row = 2, column = 0, sticky = 'nswe')
            button_nuova_lettura = tk.Button(self.popup, text = 'Nuova Lettura', font = font, command = lambda : [self.popup.destroy(), self.video_detection()])
            button_nuova_lettura.grid(row = 2, column = 1, sticky = 'nswe')   

            self.popup.mainloop()

    def insert_video_record(self):
        """Inserisce articolo e quantita' rilevati, ed eventualmente modificati, nel file selezionato"""

        file = self.vd_master.master.files_command_panel.scelta_files.get()
        if file not in self.vd_master.master.files_manager.files:
            messagebox.showerror(title = 'Errore!', message = 'Seleziona un File esistente.')
            self.popup.destroy()
        else:
            self.vd_master.master.files_manager.insert_file(file)

            art = self.entry_art.get()
            qty = self.entry_qty.get()

            #ulteriore controllo perche le entries possono essere modificate a seguito della lettura barcodes
            if check_art(art) == True and check_qty(qty) == True:
                self.vd_master.master.files_manager.files[file].insert_record((art, qty))
            else:
                messagebox.showerror(title = 'Errore!', message = 'Articolo e\o quantita\' non validi.')
            
            self.popup.destroy()
            self.video_detection()

    def video_detection(self, debug: int = 0) -> list:
        """Rileva barcodes/QRcodes dalla webcam del PC e ritorna i testi decodificati.

        Args:
            debug (int): un intero usato come flag per il debug purpose (default value: 0).

        Returns:
            decoded_text_list (list): lista contenente i testi decodificati di barcodes/QRcodes.
        """

        # apertura della videocamera
        camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        # rileva i frame della webcam in loop
        while True:
           #registra un frame dalla webcam
           _, frame = camera.read()

           # Converte il frame in scala di grigi
           gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

           # rileva e decodifica barcodes/QRcodes in frame in scala di grigi
           decoded_info = pyzbar.decode(gray_frame)       

           # per ogni barcode/QRcode decodificato, inserisce il rettangolo nel frame.
           # dopo inserisce il testo decodificato in una lista.
           decoded_text = set()
           for code in decoded_info:
                # estrae le coordinate del rettangolo di selezione e i dati di barcodes/QRcodes 
                (x, y, w, h) = code.rect
                data = code.data.decode("utf-8")
                decoded_text.add(data)

                # inserisce il testo decodificato nel frame
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                thickness = 1
                text_size, _ = cv2.getTextSize(text = data, fontFace = font, fontScale = font_scale, thickness = thickness)
                cv2.putText(
                     img = frame, 
                     text = data, 
                     org = (x, y - text_size[1]), 
                     fontFace = font, 
                     fontScale = font_scale, 
                     color = (0, 0, 255), 
                     thickness = thickness,
                     lineType = cv2.LINE_AA,
                )

                # disegna il rettangolo di selezione intorno il barcode/QRcode nel frame
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)        

           #mostra il frame con il barcodes/QRcodes rilevato
           cv2.imshow('Frame', frame)
            
           if len(decoded_text) == 2:
               camera.release() #rilascia la webcam
               cv2.destroyAllWindows() #chiude la finestra
               decoded_text_list = list(decoded_text)
               self.show_popup(decoded_text_list)

            #esce dal loop se viene premuto X in alto a dx della pc camera
           if cv2.waitKey(1) and cv2.getWindowProperty('Frame', cv2.WND_PROP_VISIBLE) < 1:
               camera.release()
               cv2.destroyAllWindows()
               decoded_text_list = []
               break

        return decoded_text_list

    