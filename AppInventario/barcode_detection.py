"""This module contains a test for reading different barcodes/QRcodes from an image.

After the detection and the decoding all the data is printed to the command prompt.

Dependencies:
    cv2 (openCV library for computer vision)
    pyzbar (libreria per riconoscimento di barcode)
        1. installa zbar per Windows (sia programma che librerie)
        2. fai riferimento ad issues (https://github.com/NaturalHistoryMuseum/pyzbar/issues/93)
        3. scarica "vcredist_x64.exe" (Visual Studio C++ 2013)
        4. esecuzione comando "pip install pyzbar"
        5.opzionale aggiungi a path del sistema cartella bin di zbar 
"""

import cv2
from pyzbar import pyzbar

def QR_barcode_detection(image_path: str, debug: int = 0) -> list:
    """Detect barcodes/QRcodes in an image and returns their decoded texts.

    Args:
        image_path (str): A string representing the image path.
        debug (int): An integer used ad flag for debug purpose (default value: 0).

    Returns:
        decoded_text_list (list): List containing the decoded texts of barcodes/QRcodes in an image.
    """

    image = cv2.imread(filename=image_path)  # Loads an image from its path and returns it (image is type "class 'numpy.ndarray'").
    if debug:
        print('\nimage_matrix:\n', image)

    gray_image = cv2.cvtColor(src= image, code= cv2.COLOR_BGR2GRAY) # Convert the image to grayscale
    if debug:
        print('\ngray_image:\n', gray_image)

    decoded_info = pyzbar.decode(gray_image)   # Detect and decode barcodes/QRcodes in the grayscale image
    if debug:
        print('\ndecoded_info:\n', decoded_info) 

    # For every decoded barcodes/QRcodes, put the rectangle in the image matrix.
    # Then append the decoded text in a list.

    decoded_text_list = []

    for code in decoded_info:
        # Extract the bounding box coordinates and barcodes/QRcodes data
        (x, y, w, h) = code.rect
        data = code.data.decode("utf-8")
        print('decoded_text: ' + data)
        decoded_text_list.append(data)

        # Put the decoded text on the image
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        text_size, _ = cv2.getTextSize(text=data, fontFace=font, fontScale=font_scale, thickness=thickness)
        cv2.putText(
            img=image, 
            text=data, 
            org=(x, y - text_size[1]), 
            fontFace=font, 
            fontScale=font_scale, 
            color=(0, 0, 255), 
            thickness=thickness,
            lineType=cv2.LINE_AA,
        )
    
        # Draw the bounding box around the barcode/QRcode on the image
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Creates a window to show the results, then saves an image in the working folder.

    cv2.imshow('image', image)
    cv2.imwrite('barcode_result.png', image)
    cv2.waitKey(0)

    return decoded_text_list

i want to detect and decode barcode and qrcode from the pc camera instead of an image. how can i do it? 

if __name__ == '__main__':
    ret = QR_barcode_detection(image_path='barcode.png')
    print(ret)
