import cv2
import numpy as np
import math


def distance(p1, p2):
    return math.sqrt((x[0] - x[1])**2 + (y[0] - y[1])**2)


#color range for the two fingers in BGR or RGB
lower = {'red': (0, 0, 230), 'green': (0, 230, 0)}
upper = {'red': (25, 25, 255), 'green': (25, 255, 25)}
#you can also change the color as you like

#Open a simple image (in your case it will be a frame)
img = cv2.imread("Meriem.jpg")

#create a white image having the same size of the frame, in order to draw
# counters to check if the algorithm detect effeciently the colors of the fingers.
# you can omit this step, but you have to be sure of the performance of your detection.
im2 = np.array(img)
im2[:] = 255

#detecte the red colore
mask = cv2.inRange(img, lower["red"], upper["red"])
#close the holes if we have detection-noises
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((10, 10), np.uint8))
#extract counter for the red color
_a, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

#same thing for the second colore
mask = cv2.inRange(img, lower["green"], upper["green"])
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((10, 10), np.uint8))
contours += cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

x = [0, 0]
y = [0, 0]
radius = [0, 0]
#foreach counter do :
for i in range(0, len(contours)):
    #draw counter in im2 with blach (0,0,0) color and width 2
    cv2.drawContours(im2, contours, i, (0, 0, 0), 2)
    #extracte the minimum enclosing circle of our shape or counter
    ((x[i], y[i]), radius[i]) = cv2.minEnclosingCircle(contours[i])
    #draw the circle in the real image (frame)
    cv2.circle(img, (int(x[i]), int(y[i])), int(radius[i]), (255, 255, 255), 2)

print(distance(x, y))

#show results
cv2.imshow("result", im2)
cv2.imshow("resultImage", img)

cv2.waitKey(0)
cv2.destroyAllWindows()