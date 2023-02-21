"""This module contains a test for reading different QR Code from an image.

After the detection and the decoding all the data is printed to the command prompt.

Dependencies:
    cv2 (openCV library for computer vision)
"""

import cv2
#print(cv2.__version__)  # Test: 4.7.0

def QR_detection(image_path: str, debug: int = 0) -> list:
    """Detect QR Codes in an image and returns their decoded texts.

    Args:
        image_path (str): A string representing the image path.
        debug (int): An integer used ad flag for debug purpose (default value: 0).

    Returns:
        decoded_text_list (list): List containing the decoded texts of QR Codes in an image.
    """

    image = cv2.imread(filename=image_path)  # Loads an image from its path and returns it (image is type "class 'numpy.ndarray'").
    if debug:
        print('\nimage_matrix:\n', image)

    decoder = cv2.QRCodeDetector()  # Creates a QRCodeDetector instance.
    if debug:
        print('\ndecoder:\n', decoder)
    
    # Uses decoder method 'detectAndDecodeMulti()' to detect and decode multiple QR Code in the image.
    # This method returns a tuple, which is deconstructed in 4 variables.

    ret_val, decoded_info, points, straight_qrcode = decoder.detectAndDecodeMulti(image)
    if debug:
        print('\nret_val:\n', ret_val)
        print('\ndecoded_info:\n', decoded_info)
        print('\npoints:\n', points)    #type: <class 'numpy.ndarray'>
        print('\nstraight_qrcode:\n', straight_qrcode)

    # Draws on the image matrix rectangles for every QR Code.

    image = cv2.polylines(img=image, pts=points.astype(int), isClosed=True, color=(0, 255, 0), thickness=3)

    # For every decoded QR Code, put the decoded text in the image matrix.
    # Then append the decoded text in a list.

    decoded_text_list = []
    for decoded_text, point in zip(decoded_info, points):
        print('decoded_text: ' + decoded_text)
        decoded_text_list.append(decoded_text)

        image = cv2.putText(
            img=image,
            text=decoded_text,
            org=point[0].astype(int),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 0, 255),
            thickness=2,
            lineType=cv2.LINE_AA,
        )

    # Creates a window to show the results, then saves an image in the working folder.

    cv2.imshow('image', image)
    cv2.imwrite('qr_result.png', image)
    cv2.waitKey(0)

    return decoded_text_list

if __name__ == '__main__':
    ret = QR_detection(image_path='qr_codes.png')
    print(ret)