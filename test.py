@@ -1,8 +1,6 @@
import numpy as np
import cv2
import math
import setinterval as setI
import threading


def distance(p1, p2):
@ -45,78 +43,36 @@ def detectColor(key, hsv, frame):
lower = {
    'blue': (70, 80, 117),
    'yellow': (23, 40, 80)
}  # assign new item lower['blue'] = (93, 10, 0)
}  #assign new item lower['blue'] = (93, 10, 0)
upper = {'blue': (150, 255, 255), 'yellow': (54, 255, 255)}

# define standard colors for circle around the object
colors = {'blue': (255, 0, 0), 'yellow': (0, 255, 217), 'cursor': (50, 50, 50)}
colors = {'blue': (255, 0, 0), 'yellow': (0, 255, 217)}

#  webcam
camera = cv2.VideoCapture(0)
sprayBlue = cv2.imread("Images/tools.png")
sprayBlue = cv2.resize(sprayBlue,(0,0), fx=0.3, fy=0.3)
hight, width,ggg=sprayBlue.shape
print(sprayBlue.shape)
# cv2.imshow("hello",sprayBlue)

p1 = [0, 0]
p2 = [0, 0]
radius = [0, 0]
firstTime = True
drawSize = 15
shift = 0
endArc = 0


def delayAnimationColors(shiftStop):
    global shift
    if shift + 1 < shiftStop:
        shift += 1
    else:
        shift = shiftStop
    # print(shift)


def delayAnimationSelectColor():
    global endArc
    global CursorImg
    if endArc + 1 < 360:
        endArc += 1
    else:
        endArc = 360
    cv2.ellipse(CursorImg, (256, 256), (50, 50), 0, 0, endArc, 255, 2)


inter = setI.setInterval(0.04, delayAnimationColors, hight)
t = threading.Timer(10, inter.cancel)
t.start()

drawSize=15
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    frame = cv2.flip(frame, 1)
    CursorImg = np.array(frame)
    rows, cols, channels = CursorImg.shape
    CursorImg[:] = 0
    #shift = 42
    CursorImg[(
        rows - shift
    ):rows, 0:width] = sprayBlue[0:shift, 0:width]
    if firstTime:
        vertualPaper = np.array(frame)
        vertualPaper[:] = 255
        firstTime = False

        inter = setI.setInterval(0.008, delayAnimationSelectColor)
        t = threading.Timer(3, inter.cancel)
        t.start()

    # color space
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # for each color in dictionary check object in frame
    #for each color in dictionary check object in frame

    p1[0], p1[1], radius[0] = detectColor("blue", hsv, frame)
    p2[0], p2[1], radius[1] = detectColor("yellow", hsv, frame)
@ -133,32 +89,31 @@ while True:

        cv2.circle(frame, (p2[0], p2[1]), radius[1], colors["yellow"], 2)

    dist = distance(p1, p2)
    midX, midY = middel(p1, p2)
    dist=distance(p1, p2)
    midX,midY=middel(p1, p2)

    # cursor
    #cursor
    if dist < 70:
        cv2.line(CursorImg, (midX + 10, midY), (midX - 10, midY),
                 colors["cursor"], 2)
        cv2.line(CursorImg, (midX, midY + 10), (midX, midY - 10),
                 colors["cursor"], 2)
    # draw
        cv2.line(CursorImg,(midX+10,midY),(midX-10,midY),colors["yellow"],2)
        cv2.line(CursorImg,(midX,midY+10),(midX,midY-10),colors["yellow"],2)
    #draw
    if dist < 50:
        cv2.circle(vertualPaper, middel(p1, p2), drawSize, colors["blue"], -1)
        cv2.circle(vertualPaper ,middel(p1, p2), drawSize, colors["blue"],-1)
    

    # Draw cursor
    rows, cols, channels = CursorImg.shape
    rows,cols,channels = CursorImg.shape
    # Now create a mask of the cursor and create its inverse mask also
    img2gray = cv2.cvtColor(CursorImg, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)
    img2gray = cv2.cvtColor(CursorImg,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    # Now black-out the area of the cursor in the vertualPaper
    img1_bg = cv2.bitwise_and(vertualPaper, vertualPaper, mask=mask_inv)
    img1_bg = cv2.bitwise_and(vertualPaper,vertualPaper,mask = mask_inv)
    # Take only region of cursor from CursorImg.
    img2_fg = cv2.bitwise_and(CursorImg, CursorImg, mask=mask)
    # Put cursor in vertualPaper
    result = cv2.add(img1_bg, img2_fg)

    img2_fg = cv2.bitwise_and(CursorImg,CursorImg,mask = mask)
    # Put cursor in vertualPaper 
    result = cv2.add(img1_bg,img2_fg)    
  
    cv2.imshow("Frame", frame)
    cv2.imshow("Frame2", result)

@ -169,4 +124,4 @@ while True:

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
cv2.destroyAllWindows()