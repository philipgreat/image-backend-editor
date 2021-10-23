
import numpy as np
import cv2

image_path='images/process.jpg'

img = cv2.imread(image_path)


#print(img)


#if img == None: 
#    raise Exception("could not load image !"+image_path)

imgGry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
height, width, channels = img.shape

ratio=800/width



ret , thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
_, contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


# sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * image.shape[1] )


sortedContours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * img.shape[1] )


counter=0

style=""
html=""


for contour in sortedContours:
    approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
    #cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5
    if len(approx) == 1000:
        cv2.putText( img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0) )
    elif len(approx) == 4 :
        x, y , w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        #print(aspectRatio)
        if h>10:
            #counter=counter+1
            #print("values-{:.0f} ".format(counter), x, y,w,h )
            #print("values-{:.0f} ".format(counter), x*ratio, y*ratio,w*ratio,h*ratio )
            #print("values-{:.0f} ".format(counter),"left: ","{:.02f}px;".format(x*ratio), "top: ","{:.02f}px;".format(y*ratio), "width: ","{:.02f}px;".format(w*ratio-5), "height: ","{:.02f}px;".format(h*ratio) )
            subArea = imgGry[y+2:y+h-4,x+2:x+w-4]

            mask = cv2.inRange(subArea, 0, 127)
            cv2.imwrite('/var/www/html/upload/mask-{:.0f}.png'.format(counter), mask)
            color_count = cv2.countNonZero(mask)
            #print("count =={:.0f} ".format( color_count) )  
            if color_count==0:
                #print("values-{:.0f} ".format(counter),"left: ","{:.02f}px;".format(x*ratio), "top: ","{:.02f}px;".format(y*ratio), "width: ","{:.02f}px;".format(w*ratio-5), "height: ","{:.02f}px;".format(h*ratio) )
                
                #parameters=(left=x*ratio-2,top=y*ratio-2,width=w*ratio+4,height=h*ratio+4,cellNumber=counter);
                template='<div style="position: absolute;overflow: hidden;padding: 0px;left:{left}px; top:{top}px; width:{width}px; height:{height}px;"></div>';
                #print(template.format(left=x*ratio-2,top=y*ratio-2,width=w*ratio+4,height=h*ratio+4,cellNumber=counter))
                styletemplate='#cell{cellNumber} {{\n\tposition: absolute;\n\toverflow: hidden;\n\tpadding: 0px;\n\tleft: {left:.0f}px; \n\ttop: {top:.0f}px; \n\twidth: {width:.0f}px; \n\theight: {height:.0f}px;\n}}\n'
                style=style+styletemplate.format(left=x*ratio-2,top=y*ratio-2,width=w*ratio+4,height=h*ratio+4,cellNumber=counter)
                html=html+'<div id="cell{counter}">cell{counter} </div>\n'.format(counter=counter)


                
                counter=counter+1
                cv2.putText(img, "rectangle {:.0f}".format(counter), (x+10, y+20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255))
    

print(style)
print(html)


#cv2.imshow('shapes', img)
#cv2.imwrite('/var/www/html/upload/rect.png', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
