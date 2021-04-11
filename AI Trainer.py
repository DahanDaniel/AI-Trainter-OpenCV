import cv2
import numpy as np
import time
import PoseModule as pm
 
cap = cv2.VideoCapture(0)
 
detector = pm.poseDetector()
countR, countL = 0, 0
dir = 0
pTime = 0
while True:
    success, img = cap.read()
    height, width, channels = img.shape
    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    if len(lmList) != 0:
        # Right Arm
        angleR = detector.findAngle(img, 12, 14, 16,False)
        if angleR >= 180:
            perR = np.interp(angleR, (200, 310), (0, 100))
            barR = np.interp(angleR, (200, 310), (int(0.9*height), int(0.1*height)))
        elif angleR < 180:
            perR = np.interp(angleR, (50, 160), (100, 0))
            barR = np.interp(angleR, (50, 160), (int(0.1*height), int(0.9*height)))
        
        # Left Arm
        angleL = detector.findAngle(img, 11, 13, 15,False)
        if angleL >= 180:
            perL = np.interp(angleL, (200, 310), (0, 100))
            barL = np.interp(angleL, (200, 310), (int(0.9*height), int(0.1*height)))
        elif angleL < 180:
            perL = np.interp(angleL, (50, 160), (100, 0))
            barL = np.interp(angleL, (50, 160), (int(0.1*height), int(0.9*height)))

 
        # Check for the dumbbell curls
        colorR = (255, 0, 255)
        if perR == 100:
            colorR = (0, 255, 0)
            if dir == 0:
                countR += 0.5
                dir = 1
        if perR == 0:
            colorR = (0, 255, 0)
            if dir == 1:
                countR += 0.5
                dir = 0
 
        colorL = (255, 0, 255)
        if perL == 100:
            colorL = (0, 255, 0)
            if dir == 0:
                countL += 0.5
                dir = 1
        if perL == 0:
            colorL = (0, 255, 0)
            if dir == 1:
                countL += 0.5
                dir = 0
        
        
        # Draw Bar
        cv2.rectangle(img, (int(0.05*width), int(0.1*height)), (int(0.15*width), int(0.9*height)), colorR, 3)
        cv2.rectangle(img, (int(0.05*width), int(barR)), (int(0.15*width), int(0.9*height)), colorR, cv2.FILLED)
        cv2.putText(img, f'{int(perR)} %', (int(0.05*width), int(0.1*height)), cv2.FONT_HERSHEY_PLAIN, 2,
                    colorR, 4)
 
        cv2.rectangle(img, (int(0.85*width), int(0.1*height)), (int(0.95*width), int(0.9*height)), colorL, 3)
        cv2.rectangle(img, (int(0.85*width), int(barL)), (int(0.95*width), int(0.9*height)), colorL, cv2.FILLED)
        cv2.putText(img, f'{int(perL)} %', (int(0.8*width), int(0.1*height)), cv2.FONT_HERSHEY_PLAIN, 2,
                    colorL, 4)
 
        
        # # Draw Curl Count
        # cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED) # Need to adjust coordinates of text
        # cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
        #             (255, 0, 0), 25)
 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
    #             (255, 0, 0), 5)
 
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    
    if cv2.waitKey(40) == 27: #esc to quit
        break
  
cv2.destroyAllWindows()
cap.release()