#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import argparse
import cv2
#import cv2 as CV #eğer python2 kullanıyorsanız eklemek zorundasınız aksi halde hata alırsınız
import time
from pymavlink import mavutil

cap = cv2.VideoCapture(0) # webcamin bagli oldugu yer

master = mavutil.mavlink_connection(
            '/dev/ttyACM0',
            baud=115200)
# Restart the ArduSub board !
def set_rc_channel_pwm(id, pwm=1500):
  
    if id < 1:
        print("Channel does not exist.")
        return

    # 8 channelimiz var
    #http://mavlink.org/messages/common#RC_CHANNELS_OVERRIDE
    if id < 9:
        rc_channel_values = [65535 for _ in range(8)]
        rc_channel_values[id - 1] = pwm
        master.mav.rc_channels_override_send(
            master.target_system,                # target_system
            master.target_component,             # target_component
            *rc_channel_values)                  # RC channel list, in microseconds.

while(True):
	# goruntu yakalama
	ret, frame = cap.read()

	# goruntuyu grilestir
			
	output = frame.copy()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	# goruntuyu blurlastir
	gray = cv2.GaussianBlur(gray,(5,5),0);
	gray = cv2.medianBlur(gray,5)

	gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,3.5)
	
	kernel = np.ones((5,5),np.uint8)
	gray = cv2.erode(gray,kernel,iterations = 1)

	gray = cv2.dilate(gray,kernel,iterations = 1)

	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 400, param1=40, param2=45, minRadius=0, maxRadius=0) # python3 icin 
  # circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 400, param1=40, param2=45, minRadius=0, maxRadius=0) #python2 icin
	# kalibre
	# daireyi isle
	
	if circles is not None:
		# x y kordinatlarini integer cevir
		circles = np.round(circles[0, :]).astype("int")
		
		
		for (x, y, r) in circles:
	
			cv2.circle(output, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

			
			print ("X kordinat: ")
			print (x)
			print ("Y Kordinat: ")
			print (y)
			print ("Radius: ")
			print (r)
			cv2.imshow('frame',output)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break



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
