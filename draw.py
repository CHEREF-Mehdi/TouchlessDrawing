import numpy as np
import cv2

cap = cv2.VideoCapture(0)

#color range for the two fingers in BGR or RGB
lower = {'red':(50, 30, 120), 'green':(0, 230, 0)} 
upper = {'red':(110,100,225), 'green':(25,255,25)}

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.flip(frame, 1)
    #frame = cv2.flip(gray, 1)
    #im2=np.array(frame)
    #im2[:] = 255
    #mask = cv2.inRange(frame, lower["red"], upper["red"])
    # Display the resulting frame
    cv2.imshow('frame', frame)
    #cv2.imshow('frame2', gray)
    b,g,r=cv2.split(frame)
    cv2.imshow('R-RGB',r)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()