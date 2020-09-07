import cv2   
import numpy as np
import pandas
from datetime import *
import csv
import matplotlib.pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from bokeh.io import show, output_file
from bokeh.plotting import figure
import random
from picamera.array import PiRGBArray
from picamera import PiCamera

#capturing video through webcam
cap=cv2.VideoCapture(0)
lis=['e501','e502','e503','e504','e505']
sender_address = 'vertex.iot@gmail.com'
sender_pass = 'papamummy'                                                         #information for email
receiver_address = 'tarun121919982000@gmail.com'



def rand():
    return random.randint(50,75)
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
video = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)
 
                                                # capture frames from the camera
for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    _, img = cap.read()
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    red_lower=np.array([136,87,111],np.uint8)
    red_upper=np.array([180,255,255],np.uint8)
    blue_lower=np.array([15,100,100],np.uint8)
    blue_upper=np.array([40,255,255],np.uint8)
    #defining the Range of yellow color
    green_lower=np.array([45,100,100],np.uint8)
    green_upper=np.array([60,255,255],np.uint8)
    #finding the range of red,blue and yellow color in the image
    red=cv2.inRange(hsv, red_lower, red_upper)
    blue=cv2.inRange(hsv,blue_lower,blue_upper)
    green=cv2.inRange(hsv,green_lower,green_upper)
    #Morphological transformation, Dilation
    kernal = np.ones((5 ,5), "uint8")
    red=cv2.dilate(red, kernal)
    res=cv2.bitwise_and(img, img, mask = red)
    blue=cv2.dilate(blue,kernal)
    res1=cv2.bitwise_and(img, img, mask = blue)
    green=cv2.dilate(green,kernal)
    res2=cv2.bitwise_and(img, img, mask = green)    
    #Tracking the Red Color
    (contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        
        area = cv2.contourArea(contour)
        if(area>3000):
            (x, y, w, h)=cv2.boundingRect(contour)                                        #motion detection
            img=cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 2)
            cv2.putText(img,"RED color",(x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            
    #Tracking the yellow Color
    (contours,hierarchy)=cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>3000):
            (x, y, w, h)=cv2.boundingRect(contour)                                        #motion detection
            img=cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)
            cv2.putText(img,"Critical",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))

    #Tracking the green Color
    (contours,hierarchy)=cv2.findContours(green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>3000):
            (x, y, w, h)=cv2.boundingRect(contour)                                        #motion detection
            img=cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(img,"Healthy",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,0,0))  
            
           
    #cv2.imshow("Redcolour",red)
    cv2.imshow("Color Tracking",img)
    #cv2.imshow("red",res)

    
    if cv2.waitKey(5) & 0xFF==ord('a'):
        date=str(datetime.now())
        df=pandas.read_csv("imp_data.csv")
        report=[] 
        temp=1
        while(temp==1):
            moist=rand()
            report.append(moist)
            temp=int(input("0/1"))
        new_c=date[:16]
        df[new_c]=report
        df.to_csv("imp_data.csv",index=False)
        for i in range(len(report)):
            df1=pandas.read_csv(lis[i]+".csv")
            df1.loc[1]=(date[10:16],report[i])
            df1.to_csv(lis[i]+".csv",index=False)  
        
            
    if  cv2.waitKey(2) & 0xFF == ord('y'):
        p = figure(x_range=lis, plot_height=250, title=new_c)
        p.vbar(x=lis, top=report, width=0.9)

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        output_file("bars.html")
        show(p)
        
        mail_content = ''' Moisture content of saplings has been calculated and is attached with email'''
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'DAILY UPDATE!!!'
                                                                                               
                                                                                                
        message.attach(MIMEText(mail_content, 'plain'))
        attach_file_name = "bars.html"                                                         
        attach_file = open(attach_file_name, 'rb')                                     
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)                                                 
        payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
        message.attach(payload)
                                                                                              
        session = smtplib.SMTP('smtp.gmail.com', 587)                                    
        session.starttls()                                                               
        session.login(sender_address, sender_pass)                                       
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print("done")

    if cv2.waitKey(8) & 0xFF == ord('x'):
        for i in range(5):
            df3=pandas.read_csv(lis[i]+".csv")
            x=df3.Time
            y=df3.Moisture
            plt.figure(i)
            plt.plot(x, y) 
            plt.xlabel('TIME') 
            plt.ylabel('MOISTURE CONTENT')
            plt.title(lis[i])
            plt.savefig(lis[i]+'.jpg',bbox_inches='tight')
        for i in range(5):
            df3=pandas.read_csv(lis[i]+".csv")
            x=df3.Time
            y=df3.Moisture
            plt.plot(x, y) 
            plt.xlabel('TIME') 
            plt.ylabel('MOISTURE CONTENT')
            if i==4:
                plt.title('Blue-e501 Orange-e502 Green-e503 Red-e504 Violet-e505')
            if i==4:
                plt.savefig('mixed_graph.jpg',bbox_inches='tight')
        print("Graphs made!!!")
        
    if cv2.waitKey(3) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows
        break
          

    
