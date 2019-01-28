import numpy as np
import cv2
import math
import setinterval as setI
import threading


def distance(p1, p2):
    if p1[0]==-1 or p2[0]==-1 :
        return 10000
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


def toolAnimation(shiftStop,up):
    global shift
    if up:
        if shift < shiftStop:
            shift += 1
        else:
            shift = shiftStop
    else :
        if shift > shiftStop:
            shift -= 1
        else:
            shift = shiftStop

def selectBackground(Nbackground):
    global endArc,application
    x=720
    y=120*(Nbackground+1)+60
    if endArc < 360:
        endArc += 1
        cv2.ellipse(application, (x, y), (30, 30), 0, 0, endArc, 255, 2)


def selectFromToolAnimation():
    global endArc,p1,CursorImg,okay

    if endArc < 360:
        endArc += 1
        cv2.ellipse(CursorImg, (p1[0], p1[1]), (10, 10), 0, 0, endArc, 255, 2)    
    else :
        CursorImg[p1[1]-11:p1[1]+12,p1[0]-11:p1[0]+12]=okay

def selectedColor(distance,rows,cols):
    global toolHight,offset,shift,ToolAnimInterval,p1
    # print(rows-toolHight)
    # print(cols)
    selectedcolor=-1
    if distance>60 and p1[1]>(rows-toolHight) and  p1[0]>=offset and p1[0]<=(cols-offset) :

        if shift==5 :
            #print("start up Animation")                
            if  ToolAnimInterval!=None :
                ToolAnimInterval.cancel()
            ToolAnimInterval = setI.setInterval(0.02, toolAnimation, *(toolHight,True))
            t = threading.Timer(1.5, ToolAnimInterval.cancel)
            t.start()

        elif shift==toolHight :                
            selectedcolor=int((p1[0]-offset)/toolHight)
            #print("selected color "+str(selectedcolor))

    elif shift==toolHight :
        #print("start dawn Animation")
        if ToolAnimInterval!=None :
            ToolAnimInterval.cancel()
        ToolAnimInterval = setI.setInterval(0.02, toolAnimation, *(5,False))
        t = threading.Timer(1.5, ToolAnimInterval.cancel)
        t.start()

    return selectedcolor
            
def menu():
    cv2.rectangle(application,(640,120),(800,240),(255,255,255),-1)
    application[244:352,645:795]=papillon_Min
    application[362:480,665:783]=bird_Min
    application[482:598,665:781]=complexe_Min

# define the lower and upper boundaries of the colors in the HSV color space
lower = {'blue': (70, 80, 117), 'yellow': (23, 40, 80)}
upper = {'blue': (150, 255, 255), 'yellow': (54, 255, 255)}

# define standard colors for circle around the object
colors = {'blue': (255, 0, 0), 'yellow': (0, 255, 217), 'cursor': (50, 50, 50)}

sprayColor=[(0, 0, 0),(203,67,0),(19,203,0),(0,114,255),(0,0,213),(11,241,255),(255,255,255)]

#  webcam
camera = cv2.VideoCapture(0)

# tool bar
sprayTool = cv2.imread("tools.png")
sprayTool = cv2.resize(sprayTool, (0, 0), fx=0.3, fy=0.3)
toolHight, toolWidth, X = sprayTool.shape

okay = cv2.imread("ok.png")
okay = cv2.resize(okay, (0, 0), fx=0.09, fy=0.09)

touchless = cv2.imread("touchless.jpg")
touchless = cv2.resize(touchless, (0, 0), fx=0.99, fy=0.99)

blanc=np.zeros((480,640,3), np.uint8)
blanc[:] = 255

papillon=cv2.imread("papillon.jpg")
papillon_Min=cv2.resize(papillon, (0, 0), fx=0.25, fy=0.25)
blanc[25:458,20:620]=papillon
papillon=blanc

blanc=np.zeros((480,640,3), np.uint8)
blanc[:] = 255

bird=cv2.imread("animaux_mini.jpg")
bird_Min=cv2.resize(bird, (0, 0), fx=0.155, fy=0.155)
bird=cv2.imread("animaux.jpg")
blanc[0:480,80:560]=bird
bird=blanc

blanc=np.zeros((480,640,3), np.uint8)
blanc[:] = 255

complexe=cv2.imread("complex_mini.jpg")
complexe_Min=cv2.resize(complexe, (0, 0), fx=0.155, fy=0.155)
complexe=cv2.imread("complex.jpg")
blanc[0:480,80:560]=complexe
complexe=blanc

blanc=np.zeros((480,640,3), np.uint8)
blanc[:] = 255

papers=[blanc,papillon,bird,complexe]

p1 = [0, 0]
p2 = [0, 0]
radius = [0, 0]
firstTime = True
drawSize = 10
shift = 5
offset = 117
endArc = 0
ToolAnimInterval= None
SelectNewColorAnimInterval= None
backgroundAnimInterval= None
selectedcolor=0
TempSelectedcolor=0
background=0
TempBackground=-1


application = np.zeros((600,800,3), np.uint8)
application[:]=255

menu()

while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    frame = cv2.flip(frame, 1)
    CursorImg = np.array(frame)
    rows, cols, channels = CursorImg.shape

    CursorImg[:] = 0


    CursorImg[(rows - shift):rows, offset:cols -
              offset] = sprayTool[0:shift, 0:toolWidth]

    
    
    if firstTime:        
        firstTime = False
        papers[0][:]=255
        vertualPaper = papers[background]
        if background!=0 :
            drawSize=5
        else :
            drawSize=8

    # color space
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # for each color in dictionary check object in frame

    p1[0], p1[1], radius[0] = detectColor("blue", hsv, frame)
    p2[0], p2[1], radius[1] = detectColor("yellow", hsv, frame)

    # only proceed if the radius meets a minimum size. Correct this value for your obect's size
    if radius[0] > 0.5:
        # draw the circle on the frame,        
        cv2.circle(frame, (p1[0], p1[1]), radius[0], colors["blue"], 2)
                
    if radius[1] > 0.5:
        cv2.circle(frame, (p2[0], p2[1]), radius[1], colors["yellow"], 2)
    
    if radius[0]<=0.5 or radius[1]<=0.5 :
        dist=1000
    else :
        dist = distance(p1, p2)
        midX, midY = middel(p1, p2)
        
        # cursor
        if dist < 70:
            cv2.line(CursorImg, (midX + 10, midY), (midX - 10, midY),
                    colors["cursor"], 2)
            cv2.line(CursorImg, (midX, midY + 10), (midX, midY - 10),
                    colors["cursor"], 2)

        # draw
        if dist < 50:
            cv2.circle(vertualPaper, middel(p1, p2), drawSize, sprayColor[selectedcolor], -1)
    
    vertualPaper = papers[background]

    #verify if the user is choosing another color
    NewSelectedcolor=selectedColor(dist,rows, cols)

    if NewSelectedcolor!=selectedcolor:
        if shift==toolHight:
            if NewSelectedcolor!=TempSelectedcolor:
                endArc=0
                TempSelectedcolor=NewSelectedcolor

                if SelectNewColorAnimInterval!=None:
                    SelectNewColorAnimInterval.cancel()                
                SelectNewColorAnimInterval = setI.setInterval(0.004, selectFromToolAnimation)
                t = threading.Timer(1.8, SelectNewColorAnimInterval.cancel)
                t.start()
            else:
                if endArc==360:
                    selectedcolor=TempSelectedcolor       

        else :
            if SelectNewColorAnimInterval!=None:
                SelectNewColorAnimInterval.cancel() 
                SelectNewColorAnimInterval=None 
                endArc=0
    
    #check if the user changed the drawing backgroud
    if dist> 50 and p1[0]>600 :
        if p1[1]<=120:
            NewBackground=0
        elif p1[1]<=240:
            NewBackground=1
        elif p1[1]<=360:
            NewBackground=2
        else:
            NewBackground=3
                          
        if NewBackground!=TempBackground:
            if backgroundAnimInterval!=None:
                backgroundAnimInterval.cancel() 

            menu()
            endArc=0
            TempBackground=NewBackground
                           
            backgroundAnimInterval = setI.setInterval(0.012, selectBackground,NewBackground)
            t = threading.Timer(5.4, backgroundAnimInterval.cancel)
            t.start()
        else:
            if endArc==360:
                background=TempBackground  
                firstTime=True
                menu()                     
                TempBackground=-1
            

    else :
        if backgroundAnimInterval!=None:
            backgroundAnimInterval.cancel() 
            backgroundAnimInterval=None 
            endArc=0
            menu()
            TempBackground=-1

        


    # Draw cursor
    rows, cols, channels = CursorImg.shape
    # Now create a mask of the cursor and create its inverse mask also
    img2gray = cv2.cvtColor(CursorImg, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    # Now black-out the area of the cursor in the vertualPaper
    img1_bg = cv2.bitwise_and(vertualPaper, vertualPaper, mask=mask_inv)
    # Take only region of cursor from CursorImg.
    img2_fg = cv2.bitwise_and(CursorImg, CursorImg, mask=mask)
    # Put cursor in vertualPaper
    result = cv2.add(img1_bg, img2_fg)
    

    video = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    application[0:120,640:800]=video
    application[120:800,0:640]=result    
    cv2.rectangle(application,(0,0),(639,120),(0,242,255),-1)
    application[10:108,0:638]=touchless

    cv2.rectangle(application,(0,120),(640,600),(0,0,0),1)

    cv2.rectangle(application,(640,120),(800,240),(0,0,0),1)
    cv2.rectangle(application,(640,240),(800,360),(0,0,0),1)
    cv2.rectangle(application,(640,360),(800,480),(0,0,0),1)

    
    

    cv2.imshow("Touchless Drawing Application", application)
    frame=cv2.resize(frame, (0, 0), fx=0.8, fy=0.8)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
