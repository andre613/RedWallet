#!/usr/bin/env python
import pygame
from pygame.locals import *
import os
from time import sleep
import RPi.GPIO as GPIO
import sys
#import image
 
#Colours
WHITE = (255,255,255)
 
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
 
pygame.init()
pygame.mouse.set_visible(False)
#lcd = pygame.display.set_mode((320, 240))
lcd = pygame.display.set_mode((100, 100))
pygame.display.update()
 
#font_big = pygame.font.Font(None, 50)
 
#touch_buttons = {'1':(80,60), '2':(240,60), '3':(80,180), '4':(240,180)}
 
#for k,v in touch_buttons.items():
#    text_surface = font_big.render('%s'%k, True, WHITE)
#    rect = text_surface.get_rect(center=v)
#    lcd.blit(text_surface, rect)
 
#pygame.display.update() 
# Scan touchscreen events
while True:
	for event in pygame.event.get():
        	if(event.type is MOUSEBUTTONDOWN):
            		pos = pygame.mouse.get_pos()
            		print pos
        	elif(event.type is MOUSEBUTTONUP):
            		pos = pygame.mouse.get_pos()
            		print pos
            		#Find which quarter of the screen we're in
            		x,y = pos
  			buttonNum = None
	
        		if y < 120:
            			if x < 160:
                			sys.exit(1)
            			else:
                			sys.exit(2)
        		else:
            			if x < 160:
                			sys.exit(3)
            			else:
                			sys.exit(4)
	sleep(0.1)
