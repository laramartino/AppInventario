"""This module contains the VideoDetection implementation,
a class containing four methods related to barcode decoding
and inserting of detected data into FilesManager and ArticlesManager.

This module is also valid for QRcodes.

Dependencies:
    cv2 (OpenCV): open source computer vision and machine learning software library.
    pyzbar: library that reads one-dimensional barcodes using the zbar library.
    tkinter
    check_values: module containing the implementation of functions that check the values of article, new article and quantity detected.
    PIL (Python Imaging Library): library for opening, manipulating and saving many different image file formats.
"""

import cv2
from pyzbar import pyzbar
from check_values import *
import tkinter as tk
from tkinter import messagebox 
from PIL import ImageGrab

class VideoDetection:
    """VideoDetection is a class with four methods related to barcode decoding 
    and inserting of detected data into FilesManager and ArticlesManager.

    Attributes:
        entry_art (None): in the methods it becomes an entry for manipulating the detected article.
        entry_qty (None): in the methods it becomes an entry for manipulating the detected quantity.
        popup (None): in the methods it becomes a tk.Toplevel.
    """

    def __init__(self, master_window: tk.Tk):
        """Initialize VideoDetection with master_window.

        Arg:
            master_window (tk.Tk): master application.
        """

        self.vd_master = master_window 

        self.entry_art = None 
        self.entry_qty = None
        self.popup = None
        self.last_decoded_text = set()

    def show_popup(self, decoded_text_list: list):
        """When barcodes are detected, a tk.Toplevel with two entries and two buttons appears.

        Arg:
            decoded_text_list (list): list containing the article and the quantity to insert.
        """

        if check_art(decoded_text_list[0]) == True and check_qty(decoded_text_list[1]) == True:
            art = decoded_text_list[0]
            qty = decoded_text_list[1]
        elif check_art(decoded_text_list[1]) == True and check_qty(decoded_text_list[0]) == True:
            qty = decoded_text_list[0]
            art = decoded_text_list[1]
        else:
            messagebox.showerror(title='Errore!', message='Articolo e\o quantita\' non validi.')
            return

        if set(decoded_text_list) == self.last_decoded_text:
            messagebox.showwarning(title='Attenzione!', message='Record appena inserito.')

        self.popup = tk.Toplevel()
        self.popup.title('Codici rilevati')
        self.popup.geometry('600x300+200+200')
        self.popup.resizable(False, False)  # Popup size cannot be changed by the user.

        font = 'calibri 20'
        padx = 10
        pady = 30

        self.popup.rowconfigure(index=0, weight=1)
        self.popup.rowconfigure(index=1, weight=1)
        self.popup.rowconfigure(index=2, weight=1)
        self.popup.columnconfigure(index=0, weight=1)
        self.popup.columnconfigure(index=1, weight=1)

        label_art = tk.Label(self.popup, text='Articolo: ', font=font)
        label_art.grid(row=0, column=0, sticky='nswe')
        self.entry_art = tk.Entry(self.popup, font=font)
        self.entry_art.grid(row=0, column=1, sticky='nswe', padx=padx, pady=pady)
        self.entry_art.insert(0, art)
        self.entry_art.bind('<Button-1>', show_keyboard)
        label_qty = tk.Label(self.popup, text='Qty: ', font=font)
        label_qty.grid(row=1, column=0, sticky='nswe')
        self.entry_qty = tk.Entry(self.popup, font=font)
        self.entry_qty.grid(row=1, column=1, sticky='nswe', padx=padx, pady=pady)
        self.entry_qty.insert(0, qty)
        self.entry_qty.bind('<Button-1>', show_keyboard)

        button_insert = tk.Button(self.popup, text='Aggiungi', font=font, command=self.insert_video_record)
        button_insert.grid(row=2, column=0, sticky='nswe')
        button_new_detection = tk.Button(self.popup, text='Nuova Lettura', font=font, command=lambda: [self.popup.destroy(), self.video_detection()])
        button_new_detection.grid(row=2, column=1, sticky='nswe')   
                
        self.popup.mainloop()

    def insert_video_record(self):
        """Insert article and quantity detected in the selected file."""

        selected_file = self.vd_master.master.files_command_panel.files_choice.get()
        if selected_file not in self.vd_master.master.files_manager.files:
            messagebox.showerror(title='Errore!', message='Seleziona un File esistente.')
            self.popup.destroy()
        else:
            self.vd_master.master.files_manager.insert_file(selected_file)

            art = self.entry_art.get()
            qty = self.entry_qty.get()

            # Another check because the entries can be modified after detection.
            if check_art(art) == True and check_qty(qty) == True:
                self.vd_master.master.files_manager.files[selected_file].insert_record((art, qty))
                self.last_decoded_text = {art, qty}
            else:
                messagebox.showerror(title = 'Errore!', message = 'Articolo e\o quantita\' non validi.')
            
            self.popup.destroy()
            self.video_detection()

    def video_detection(self, debug: int=0) -> list:
        """Detect barcodes from the PC camera and returns their decoded texts.

        Arg:
            debug (int): an integer used as a flag for debug purpose (default value: 0).

        Return:
            decoded_text_list (list): list containing the decoded texts of barcodes.
        """

        screen = ImageGrab.grab()  # Capture the screen's contents as an image.
        screen_width, screen_height = screen.size 

        camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # Open the PC camera.

        # Loop over frames from the camera.
        while True:
          
           _, frame = camera.read()  # Capture a frame from the camera.

           if screen_height > screen_width:
              frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  # Rotation of the PC camera if the tablet is used in portrait mode.

           gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale.

           decoded_info = pyzbar.decode(gray_frame)  # Detect and decode barcodes in the grayscale frame.

           # For every decoded barcodes, put the rectangle in the frame.
           # Then add the decoded text in a set.
           decoded_text = set()
           for code in decoded_info:
                # Extract the bounding box coordinates and barcodes data. 
                (x, y, w, h) = code.rect
                data = code.data.decode("utf-8")
                decoded_text.add(data)

                # Put the decoded text on the frame.
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                thickness = 1
                text_size, _ = cv2.getTextSize(text=data, fontFace=font, fontScale=font_scale, thickness=thickness)
                cv2.putText(
                     img=frame, 
                     text=data, 
                     org=(x, y - text_size[1]), 
                     fontFace=font, 
                     fontScale=font_scale, 
                     color=(0, 0, 255), 
                     thickness=thickness,
                     lineType=cv2.LINE_AA,
                )

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw the bounding box around the barcode on the frame.

           cv2.imshow('Frame', frame)  # Show the frame with the detected barcodes.
           
           if len(decoded_text) == 2:
               camera.release()  # Release the camera.
               cv2.destroyAllWindows()  # Close the window.
               decoded_text_list = list(decoded_text)
               self.show_popup(decoded_text_list)

           # Exit the loop if the user clicks the 'X' button at the top right of the PC camera window.
           if cv2.waitKey(1) and cv2.getWindowProperty('Frame', cv2.WND_PROP_VISIBLE) < 1:
               camera.release()
               cv2.destroyAllWindows()
               decoded_text_list = []
               break

        return decoded_text_list

    

