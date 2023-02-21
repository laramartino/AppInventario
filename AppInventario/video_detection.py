import cv2
from pyzbar import pyzbar

def video_detection(debug: int = 0) -> list:
    """Detect barcodes/QRcodes from the PC camera and returns their decoded texts.

    Args:
        debug (int): An integer used ad flag for debug purpose (default value: 0).

    Returns:
        decoded_text_list (list): List containing the decoded texts of barcodes/QRcodes.
    """

    # Open the default camera
    camera = cv2.VideoCapture(0)

    # Loop over frames from the camera
    while True:
        # Capture a frame from the camera
        _, frame = camera.read()

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect and decode barcodes/QRcodes in the grayscale frame
        decoded_info = pyzbar.decode(gray_frame)

        # For every decoded barcodes/QRcodes, put the rectangle in the frame.
        # Then append the decoded text in a list.
        decoded_text_list = []
        for code in decoded_info:
            # Extract the bounding box coordinates and barcodes/QRcodes data
            (x, y, w, h) = code.rect
            data = code.data.decode("utf-8")
            print('decoded_text: ' + data)
            decoded_text_list.append(data)

            # Put the decoded text on the frame
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

            # Draw the bounding box around the barcode/QRcode on the frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Show the frame with the detected barcodes/QRcodes
        cv2.imshow('frame', frame)

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    camera.release()
    cv2.destroyAllWindows()

    return decoded_text_list

if __name__ == '__main__':
    ret = video_detection()
    print(ret)