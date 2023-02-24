'''Questo modulo contiene l'implementazione di video_detection,
una funzione che permette la rilevazione e la decodifica di barcodes e QRcodes

Dipendenze:
    cv2 (OpenCV): libreria riguardo la visione artificiale in tempo reale
    pyzbar: libreria di supporto a cv2
'''

import cv2
from pyzbar import pyzbar
from check_valori import *

def video_detection(debug: int = 0) -> list:
    """Rileva barcodes/QRcodes dalla webcam del PC e ritorna i testi decodificati.

    Args:
        debug (int): un intero usato come flag per il debug purpose (default value: 0).

    Returns:
        decoded_text_list (list): lista contenente i testi decodificati di barcodes/QRcodes.
    """

    # apertura della videocamera
    camera = cv2.VideoCapture(0)

    # rileva i frame della webcam in loop
    while True:
        # registra un frame dalla webcam
        _, frame = camera.read()

        # Converte il frame in scala di grigi
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # rileva e decodifica barcodes/QRcodes in frame in scala di grigi
        decoded_info = pyzbar.decode(gray_frame)

        # per ogni barcode/QRcode decodificato, inserisce il rettangolo nel frame.
        # dopo inserisce il testo decodificato in una lista.
        decoded_text_list = []
        for code in decoded_info:
            # estrae le coordinate del rettangolo di selezione e i dati di barcodes/QRcodes 
            (x, y, w, h) = code.rect
            data = code.data.decode("utf-8")
            #print('decoded_text: ' + data)
            decoded_text_list.append(data)
        

            # inserisce il testo decodificato nel frame
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

            # disegna il triangolo di selezione intorno il barcode/QRcode nel frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # mostra il frame con il barcodes/QRcodes rilevato
        cv2.imshow('frame', frame)

        #esce dal loop se viene premuto sulla tastiera 'q' 
        if cv2.waitKey(1) & 0xFF == ord('q'):
           break

    # Rilascia la webcam e chiude la finestra
    camera.release()
    cv2.destroyAllWindows()

    return decoded_text_list

if __name__ == '__main__':
    ret = video_detection()
    print(ret)