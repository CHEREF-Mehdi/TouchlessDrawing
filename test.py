import numpy as np
import cv2
import math


def distance(p1, p2):
    return int(math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2))


def middel(p1, p2):
    return (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2))


def detectColor(key, hsv, frame):
    # construct a mask for the color from dictionary`1, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.inRange(hsv, lower[key], upper[key])
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    x, y, radius = 0, 0, 0

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        return (int(x), int(y), int(radius))

    return (x, y, radius)


# define the lower and upper boundaries of the colors in the HSV color space
lower = {
    'blue': (70, 80, 117),
    'yellow': (23, 40, 80)
}  #assign new item lower['blue'] = (93, 10, 0)
upper = {'blue': (150, 255, 255), 'yellow': (54, 255, 255)}

# define standard colors for circle around the object
colors = {'blue': (255, 0, 0), 'yellow': (0, 255, 217)}

# if a video path was not supplied, grab the reference
# to the webcam
# if not args.get("video", False):
camera = cv2.VideoCapture(0)

p1 = [0, 0]
p2 = [0, 0]
radius = [0, 0]
firstTime = True
drawSize=15
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    frame = cv2.flip(frame, 1)
    CursorImg = np.array(frame)
    CursorImg[:] = 0
    if firstTime:
        vertualPaper = np.array(frame)
        vertualPaper[:] = 255
        firstTime = False
    # color space
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    #for each color in dictionary check object in frame

    p1[0], p1[1], radius[0] = detectColor("blue", hsv, frame)
    p2[0], p2[1], radius[1] = detectColor("yellow", hsv, frame)

    # only proceed if the radius meets a minimum size. Correct this value for your obect's size
    if radius[0] > 0.5:
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        cv2.circle(frame, (p1[0], p1[1]), radius[0], colors["blue"], 2)
        cv2.putText(frame, str(distance(p1, p2)),
                    (p1[0] - radius[0], p1[1] - radius[0]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, colors["blue"], 2)
    if radius[1] > 0.5:

        cv2.circle(frame, (p2[0], p2[1]), radius[1], colors["yellow"], 2)

    dist=distance(p1, p2)
    midX,midY=middel(p1, p2)

    #cursor
    if dist < 70:
        cv2.line(CursorImg,(midX+10,midY),(midX-10,midY),colors["yellow"],2)
        cv2.line(CursorImg,(midX,midY+10),(midX,midY-10),colors["yellow"],2)
    #draw
    if dist < 50:
        cv2.circle(vertualPaper ,middel(p1, p2), drawSize, colors["blue"],-1)
    

    # Draw cursor
    rows,cols,channels = CursorImg.shape
    # Now create a mask of the cursor and create its inverse mask also
    img2gray = cv2.cvtColor(CursorImg,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    # Now black-out the area of the cursor in the vertualPaper
    img1_bg = cv2.bitwise_and(vertualPaper,vertualPaper,mask = mask_inv)
    # Take only region of cursor from CursorImg.
    img2_fg = cv2.bitwise_and(CursorImg,CursorImg,mask = mask)
    # Put cursor in vertualPaper 
    result = cv2.add(img1_bg,img2_fg)    
  
    cv2.imshow("Frame", frame)
    cv2.imshow("Frame2", result)

    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()