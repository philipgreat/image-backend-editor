import numpy as np
import cv2

img = cv2.imread('images/004.png')
imgGry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
height, width, channels = img.shape

ratio=800/width



ret , thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
_, contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

counter=0

for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
    cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5
    if len(approx) == 1000:
        cv2.putText( img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0) )
    elif len(approx) == 4 :
        x, y , w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        #print(aspectRatio)
        if h>60:
            counter=counter+1
            #print("values-{:.0f} ".format(counter), x, y,w,h )
            #print("values-{:.0f} ".format(counter), x*ratio, y*ratio,w*ratio,h*ratio )
            print("values-{:.0f} ".format(counter),"left: ","{:.02f}px;".format(x*ratio), "top: ","{:.02f}px;".format(y*ratio), "width: ","{:.02f}px;".format(w*ratio-5), "height: ","{:.02f}px;".format(h*ratio) )

            cv2.putText(img, "rectangle {:.0f}".format(counter), (x+10, y+20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))


#cv2.imshow('shapes', img)
cv2.imwrite('/var/www/html/upload/rect.png', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

