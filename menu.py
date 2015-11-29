#!/usr/bin/python
import sys
import pygbutton 
import pygame
import signal

ONPI = False

if ONPI:
  os.putenv('SDL_FBDEV', '/dev/fb1')
  os.putenv('SDL_MOUSEDRV', 'TSLIB')
  os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
  pygame.init()
  pygame.mouse.set_visible(False)

DISPLAYSURFACE = pygame.display.set_mode((320,240))
FONTBIG = pygame.font.Font(None, 50)

WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,255,0)

def renderText(lines, default_color=WHITE):
  for i in range(len(lines)):
    print "Rendering text line %s"%(i+1)

    if isinstance(lines[i], tuple):
      text = FONTBIG.render(lines[i][0], True, lines[i][1])
    else:
      text = FONTBIG.render(lines[i], True, default_color)
    
    DISPLAYSURFACE.blit(text, text.get_rect(center=(160,30*(i+1))))

def MENUmain():
  return (
    (
      "Yeah this is text",
      ("New Line", RED),
      ("Next", BLUE),
      ("More", WHITE),
      "Line 5"
    ),
    (
      (pygbutton.PygButton((0, 180, 140, 60), 'Create Wallet'), MENUcreateWallet),
      (pygbutton.PygButton((180, 180, 140, 60), 'Sign Transaction'), MENUsignTransaction)
    )
  )

def MENUcreateWallet():
  return (
    ("C"),
    (
      (pygbutton.PygButton((0, 180, 140, 60), 'CANCEL'), MENUmain),
      (pygbutton.PygButton((180, 180, 140, 60), 'OK'), MENUcreateRedKey)
    )
  )

def MENUcreateRedKey():  
  return (
    ("R"),
    ( (pygbutton.PygButton((0, 180, 320, 60), 'CANCEL(RK)'), MENUmain), ) # I am a python newb, if you are too note the trailing comma to create a 1 element tuple
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
# menuOut = MENUmain()
# currentText = menuOut[0]
# currentButtons = menuOut[1]

currentText, currentButtons = MENUmain()
redraw = True

while True:

  if redraw:
    DISPLAYSURFACE.fill((0,0,0))

    renderText(currentText)

    for b in currentButtons:
      print b
      b[0].draw(DISPLAYSURFACE)

    pygame.display.update()
    redraw = False

  for event in pygame.event.get():
    for b in currentButtons: # read buttons
      if 'click' in b[0].handleEvent(event):        
        currentText, currentButtons = b[1]()
        redraw = True