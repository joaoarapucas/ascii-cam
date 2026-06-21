import cv2
import numpy as np

import os

LIGHT_LEVELS = '.,-~:;=!*#$@' # Same characters as in donut.c!

CAM_HEIGHT = 1080
CAM_WIDTH = 1920


def get_ascii_size(cols, ratio=0.5):
    """
    Calculates width and height of the output ASCII image.
    """
    
    terminal_rows = os.get_terminal_size().lines
    rows_from_cols = int((CAM_HEIGHT / CAM_WIDTH) * cols * ratio)

    # If rows fit the terminal height
    if rows_from_cols <= terminal_rows:
        return rows_from_cols, cols

    # Else adjusts both rows and columns size
    else:
        cols_adjusted = int((CAM_WIDTH / CAM_HEIGHT) * terminal_rows / ratio)
        return terminal_rows, cols_adjusted


# Number of columns and rows the output text will have
ascii_rows, ascii_cols  = get_ascii_size(os.get_terminal_size().columns)


last_cols = ascii_cols

cap = cv2.VideoCapture(0)
cap.set(3, CAM_WIDTH)
cap.set(4, CAM_HEIGHT)


while True:

    # ----- IMAGE SETUP ----- #

    ret, frame = cap.read()
    
    if not ret:
        print("no cam readings!")
        break
    
    flipped_frame = cv2.flip(frame, 1)
        
    gray_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)
    
    # Deals with window resizing
    current_cols = os.get_terminal_size().columns
    if(last_cols != current_cols):
        ascii_rows, ascii_cols = get_ascii_size(current_cols)
         
        os.system('cls' if os.name == 'nt' else 'clear')
            
    resized_frame = cv2.resize(gray_frame, (ascii_cols, ascii_rows), interpolation = cv2.INTER_AREA)
   
    cv2.imshow('black and white resized camera', resized_frame)

    print("\033[H", end="")  # Resets the console cursor

    # ----- GENERATES ASCII IMAGE ----- #

    ascii_frame = []
    for i in range(0, ascii_rows):
        char_row = []
        
        for j in range(0, ascii_cols):
            char_index = int(resized_frame[i,j] / 255 * (len(LIGHT_LEVELS) -1))
            char_row.append(LIGHT_LEVELS[char_index])
        
        ascii_frame.append("".join(char_row))

    print("\n".join(ascii_frame))  # Prints the final ascii image

            
    last_cols = current_cols

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
