#!/usr/bin/python
import os
import sys
import pygbutton 
import pygame
import signal
import subprocess
import time

if os.getenv('USER') == 'pi': 
  ONPI = True
else:
  ONPI = False

if ONPI:
  os.putenv('SDL_FBDEV', '/dev/fb1')
  os.putenv('SDL_MOUSEDRV', 'TSLIB')
  os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
DISPLAYSURFACE = pygame.display.set_mode((320,240))
pygame.mouse.set_visible(not ONPI)

FONTBIG = pygame.font.Font(None, 50)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

def renderText(lines, default_color=WHITE):
  for i in range(len(lines)):

    if isinstance(lines[i], tuple):
      text = FONTBIG.render(lines[i][0], True, lines[i][1])
    else:
      text = FONTBIG.render(lines[i], True, default_color)

    DISPLAYSURFACE.blit(text, text.get_rect(center=(160,30*(i+1))))

def MENUmain():
  return (
    (
      "Welcome to",
      ("REDWALLET", RED),
      "",
      "Please select",
      "an operation"
    ),
    (
      (pygbutton.PygButton((0, 180, 140, 60), 'Create Wallet'), MENUcreateWallet),
      (pygbutton.PygButton((180, 180, 140, 60), 'Sign Transaction'), MENUsignTransaction)
    )
  )

def MENUcreateWallet():
  return (
    (
      "",
      "",
      "Remove ALL Keys"
    ),
    (
      (pygbutton.PygButton((0, 180, 140, 60), 'CANCEL'), MENUmain),
      (pygbutton.PygButton((180, 180, 140, 60), 'OK'), MENUcreateRedKey)
    )
  )

def MENUcreateRedKey():  
  return (
    (
      "Insert the",
      "",
      ("RED", RED),
      "",
      "Key"
    ),
    (
      (pygbutton.PygButton((0, 180, 140, 60), 'CANCEL'), MENUmain),
      (pygbutton.PygButton((180, 180, 140, 60), 'OK'), MENUcreateBlueKey)
    )
  )

def MENUcreateBlueKey():  
  return (
    (
      "Insert the",
      "",
      ("BLUE", BLUE),
      "",
      "Key"
    ),
    (
      (pygbutton.PygButton((0, 180, 140, 60), 'CANCEL'), MENUmain),
      (pygbutton.PygButton((180, 180, 140, 60), 'OK'), MENUcreateKeys)
    )
  )

def MENUcreateKeys():  

  if ONPI:
    os.mkdir('/media/REDKEY')  
    os.mkdir('/media/BLUEKEY')

    subprocess.check_call('mount','/dev/sda1', '/media/REDKEY')
    subprocess.check_call('mount','/dev/sdb1', '/media/BLUEKEY')

    wallet_ts = '{0:f}'.format(time.time())
    wallet_name = 'redwallet-RED-' + wallet_ts + '_wallet'
    wallet_path = '/media/REDKEY/' + wallet_name

    subprocess.check_call('electrum', 'create', '-o', '-w', wallet_path)

    shutil.copy(wallet_path, '/run')

    subprocess.check_call('electrum', 'deseed', '-o', '-w', '/run/' + wallet_name)

    shutil.move('/run/' + wallet_name, '/media/BLUEKEY/redwallet-BLUE-' + wallet_ts + '_wallet')

    subprocess.check_call('umount', '/media/REDKEY')
    subprocess.check_call('umount', '/media/BLUEKEY')

  return (
    (
      "Wallet Created",
      "",
      "You can now",
      "REMOVE",
      "BOTH KEYS"
    ),
    ( (pygbutton.PygButton((0, 180, 320, 60), 'OK'), MENUmain), ) # I am a python newb, if you are too, note the trailing comma to create a 1 element tuple
  )

def MENUsignTransaction():
  return (
    ("S"),
    (
      (pygbutton.PygButton((0, 180, 140, 60), 'CANCEL'), MENUmain),
      (pygbutton.PygButton((180, 180, 140, 60), 'OK'), MENUcreateRedKey)
    )
  )

#Set up the main menu
currentText, currentButtons = MENUmain()
redraw = True

running = True
while running:

  if redraw:
    DISPLAYSURFACE.fill((0,0,0))
    renderText(currentText)
    for b in currentButtons:
      print b
      b[0].draw(DISPLAYSURFACE)
    pygame.display.update()
    redraw = False

  for event in pygame.event.get():

    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        running = False

    for b in currentButtons: # read buttons
      if 'click' in b[0].handleEvent(event):        
        currentText, currentButtons = b[1]()
        redraw = True
