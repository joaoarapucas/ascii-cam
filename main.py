import cv2
import numpy as np

LIGHT_LEVELS = '.,-~:;=!*#$@' #same characters as in donut.c!

CAM_HEIGHT = 1080
CAM_WIDTH = 1920


ASCII_RATIO = .5
ASCII_COLS = 170
ASCII_ROWS = int( (CAM_HEIGHT / CAM_WIDTH) * ASCII_COLS * ASCII_RATIO ) #ascii ratio (accounts for rect)

print(f"rows: {ASCII_ROWS}")

cap = cv2.VideoCapture(0)
cap.set(3, CAM_WIDTH)
cap.set(4, CAM_HEIGHT)

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("no cam readings!")
        break
    
    flipped_frame = cv2.flip(frame, 1)
    
    gray_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)

    resized_frame = cv2.resize(gray_frame, (ASCII_COLS, ASCII_ROWS), interpolation = cv2.INTER_AREA)
   
    cv2.imshow('black and white resized camera', resized_frame)

    print("\033[H", end="") #resets terminal


    ascii_frame = []
    for i in range(0, ASCII_ROWS):
        char_row = []
        for j in range(0, ASCII_COLS):
            #char index
            char = int(resized_frame[i,j] / 255 * (len(LIGHT_LEVELS) -1))

            char_row.append(LIGHT_LEVELS[char])

        ascii_frame.append("".join(char_row))

    print("\n".join(ascii_frame))


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
