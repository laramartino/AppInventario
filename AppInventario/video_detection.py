'''Questo modulo contiene l'implementazione di video_detection,
una funzione che permette la rilevazione e la decodifica di barcodes e QRcodes

Dipendenze:
    cv2 (OpenCV): libreria riguardo la visione artificiale in tempo reale
    pyzbar: libreria di supporto a cv2
    tkinter
    check_valori: modulo contenente l'implementazione di funzioni che controllano i valori di articolo e quantita' rilevati
'''

import cv2
from pyzbar import pyzbar
from check_valori import *
import tkinter as tk
from tkinter import messagebox 

class VideoDetection:

    def __init__(self, master_window: tk.Tk):
        self.vd_master = master_window 
        self.entry_art = None 
        self.entry_qty = None
        self.popup = None

    def show_popup(self, decoded_text: list):

        if check_art(decoded_text[0]) == True and check_qty(decoded_text[1]) == True:
            art = decoded_text[0]
            qty = decoded_text[1]
        elif check_art(decoded_text[1]) == True and check_qty(decoded_text[0]) == True:
            qty = decoded_text[0]
            art = decoded_text[1]
        else:
            messagebox.showerror(title = 'Errore!', message = 'Articolo e\o quantita\' non validi.')

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

        tk.Button(self.popup, text = 'Aggiungi', font = font, command = self.insert_video_record).grid(row = 2, column = 0, sticky = 'nswe')
        tk.Button(self.popup, text = 'Nuova Lettura', font = font, command = lambda: [self.popup.destroy(), self.restart_video_detection()]).grid(row = 2, column = 1, sticky = 'nswe')
        self.popup.grab_set()
        self.popup.mainloop()   
        
    def restart_video_detection(self):

        cv2.destroyAllWindows()
        self.video_detection()

    def insert_video_record(self):

        file = self.vd_master.master.files_command_panel.scelta_files.get()
        if file == '' or file == ' ':
            messagebox.showerror(title = 'Errore!', message = 'File invalido.')
            self.popup.destroy()
        else:
            self.vd_master.master.files_manager.insert_file(file)

        art = self.entry_art.get()
        qty = self.entry_qty.get()
        self.vd_master.master.files_manager.files[file].insert_record((art, qty))

        self.popup.destroy()
        cv2.destroyAllWindows()

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

           # mostra il frame con il barcodes/QRcodes rilevato
           cv2.imshow('frame', frame) 

           if len(decoded_text) == 2:
              decoded_text = list(decoded_text)
              self.show_popup(decoded_text)

            #esce dal loop se viene premuto sulla tastiera 'q' 
           if cv2.waitKey(1) and cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1:
              break
               
        # Rilascia la webcam e chiude la finestra
        #camera.release()
        cv2.destroyAllWindows()

        return decoded_text
