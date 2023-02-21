from qr_detection import QR_detection
from barcode_detection import QR_barcode_detection

if __name__=='__main__':
    funzione_chiamata=QR_barcode_detection
    ret = funzione_chiamata(image_path='barcode_QR.png')
    print(ret)