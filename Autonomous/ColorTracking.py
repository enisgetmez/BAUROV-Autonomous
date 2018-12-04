#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
import imutils
import numpy as np
import argparse
import cv2
import time
from pymavlink import mavutil

cap = cv2.VideoCapture(0) # webcamin bagli oldugu yer

master = mavutil.mavlink_connection(
            '/dev/ttyACM0',
            baud=115200) ##pixhawk ile raspberry pi arasında iletişim kurmak

def set_rc_channel_pwm(id, pwm=1500):
  
    if id < 1:
        print("Channel does not exist.")
        return

    
   
    if id < 9:
        rc_channel_values = [65535 for _ in range(8)]
        rc_channel_values[id - 1] = pwm
        master.mav.rc_channels_override_send(
            master.target_system,               
            master.target_component,             
            *rc_channel_values)                 


ret, frame = cap.read()

#sari rengin algilanmasi
colorLower = (24, 100, 100) 
colorUpper = (44, 255, 255)
#converter.py ile algılayacağınız renginizin upper ve lower değerlerini dönüştürebilirsiniz. 
camera = cv2.VideoCapture(0)
while True:

	
     (grabbed, frame) = camera.read()

     frame = imutils.resize(frame, width=600)
     frame = imutils.rotate(frame, angle=180)

     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	
     mask = cv2.inRange(hsv, colorLower, colorUpper)
     mask = cv2.erode(mask, None, iterations=2)
     mask = cv2.dilate(mask, None, iterations=2)
	
	
     cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
	 cv2.CHAIN_APPROX_SIMPLE)[-2]
     center = None
 

     if len(cnts) > 0:

		     c = max(cnts, key=cv2.contourArea)
		     ((x, y), radius) = cv2.minEnclosingCircle(c)
		     M = cv2.moments(c)
		     center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		
		     if radius > 10: #algılanacak hedefin minumum boyutu
			     cv2.circle(frame, (int(x), int(y)), int(radius),
				 (0, 255, 255), 2)
			     cv2.circle(frame, center, 5, (0, 0, 255), -1)
     print("x : ")
     print(x)
     print("y : ")
     print(y)
     print("büyüklük : ")
     print(r)

	set_rc_channel_pwm(3, 1540) # robotun sabit kalabilmesi icin
	time.sleep(5) # 5 saniyede tekrarla
    if (x == 0 and y == 0): #hedef algilanmadiysa
	     set_rc_channel_pwm(6, 1400) # kendi etrafında dön
         print("hedef algilanmadi kendi etrafimda dönüyorum...")
     elif (r < 100): # hedef yakinimizdaysa
	     set_rc_channel_pwm(5, 1600) # düz git 
	     print("Balon patlatiliyor...")
     elif (x > 360 and x < 390 and y > 240 and y < 270 ): # hedef ortadaysa
         set_rc_channel_pwm(5, 1600) # düz git
         print("Düz Gidiliyor...")

     elif (x < 360): # hedef robotun solunda kalıyorsa
         set_rc_channel_pwm(4, 1400) # sola dön komutun kontrol edilmesi lazım
          print("Sol'a dönülüyor...")
          if (y < 240):
             set_rc_channel_pwm(3, 1600 ) # robotun havalanmasi
          elif (y > 270):
             set_rc_channel_pwm(3, 1400) # robotun alcalmasi deger random girildi alcalma pwm bulunduktan sonra degistirilicek
     elif (x > 390): # hedef robotun saginda kaliyorsa
         set_rc_channel_pwm(4, 1600) # saga dön komutun kontrol edilmesi lazım
         print("Sag'a dönülüyor...")
         if (y < 240):
             set_rc_channel_pwm(3, 1600) # robotun havalanmasi
         elif (y > 270):
             set_rc_channel_pwm(3, 1400) # robotun alcalmasi deger random girildi alcalma pwm bulunduktan sonra degistirilicek
cap.release()
cv2.destroyAllWindows()
