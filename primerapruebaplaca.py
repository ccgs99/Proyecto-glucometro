import cv2 
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

placa=[]
image= cv2.imread('auto.jpg')
gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray= cv2.blur(gray,(3,3))
canny= cv2.Canny(gray,150,200)
canny= cv2.dilate(canny,None,iterations=1)
cnts,_= cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

for c in cnts:
    area= cv2.contourArea(c)
    x,y,w,h= cv2.boundingRect(c)
    epsilon= 0.05*cv2.arcLength(c,True)
    approx= cv2.approxPolyDP(c,epsilon,True)    
    if len(approx)==4 and area > 5000:
        print('area=',area)
        #cv2.drawContours(image, [c],0,(0,255,0),2)
        aspect_ratio= float(w)/h
        if aspect_ratio> 2.4:
            placa= gray[y:y+h,x:x+w]
            text=pytesseract.image_to_string(placa, config='--psm 11')
            print('text= ',text)
            cv2.imshow('placa',placa)
            cv2.moveWindow('placa',980,10)
           # cv2.drawContours(image, [c],0,(0,255,0),2)
cv2.imshow('image',image)
cv2.moveWindow('image',45,10)
cv2.waitKey(0)
