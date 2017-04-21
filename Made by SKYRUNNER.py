# program written by Joshua Koh,  joshuakoh225@gmail.com 
# for Fallon Middle School, Dublin, CA
import time
import pygame
import sys
import curses
import atexit
import pigpio # see http://abyz.co.uk/rpi/pigpio/python.html for more details

from pygame.locals import *
pi = pigpio.pi() #init the pi object

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300)) # size of the pygame windows
# pygame is used for polling the keyboard for key pressed

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
BLUE  = (  0,   0, 255)

# 4 GPIO pins are needed for the motor controller L293
# below are GPIO pin definitions
PinLF = 24  # left forward
PinLB = 18  # left forward
PinRF = 22  # right forward
PinRB = 17  # right backward


# all L293 GPIO control pins need to be output
pi.set_mode(PinLF, pigpio.OUTPUT)
pi.set_mode(PinLB, pigpio.OUTPUT)
pi.set_mode(PinRF, pigpio.OUTPUT)
pi.set_mode(PinRB, pigpio.OUTPUT) 

# speed variables, 8 bit number from 0-255
LFS = 0 # Left Forward Speed
LBS = 0 # Left Backward Speed
RFS = 0 # Right Forward Speed
RBS = 0 # Right Backward Speed

# range limit for speed
minspd = 0
maxspd = 255

pygame.display.set_caption("SKYRUNNER CONTROL")
WINDOWWIDTH = 400
WINDOWHEIGHT = 300
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
windowSurface.fill(BLACK)
DISPLAYSURF.fill(BLACK)
fontObj = pygame.font.Font('freesansbold.ttf' , 32)
textSurfaceObj = fontObj.render("LSPD    RSPD", True, WHITE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200, 150)
DISPLAYSURF.blit(textSurfaceObj, textRectObj)
pygame.display.update()

while True:
    DISPLAYSURF.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            # set speed to zero before quiting the program
            LBS = 0
            RBS = 0
            LFS = 0
            RFS = 0
            pi.set_PWM_dutycycle(PinLF, LFS)
            pi.set_PWM_dutycycle(PinLB, LBS)
            pi.set_PWM_dutycycle(PinRF, RFS)
            pi.set_PWM_dutycycle(PinRB, RBS)
            pygame.quit()
        if event.type == KEYDOWN: # key is pressed
            if (event.key == K_w): # W key pressed, full speed backward
                LFS = 255
                RFS = 255
                LBS = 0
                RBS = 0
                pi.set_PWM_dutycycle(PinLF, LFS)
                pi.set_PWM_dutycycle(PinLB, LBS)
                pi.set_PWM_dutycycle(PinRF, RFS)
                pi.set_PWM_dutycycle(PinRB, RBS)
                fontObj = pygame.font.Font('freesansbold.ttf' , 32)
                textSurfaceObj = fontObj.render('255' + '     255' , True, WHITE)
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (200, 150)
                DISPLAYSURF.blit(textSurfaceObj, textRectObj)
                pygame.display.update()
            if (event.key == K_s): # S key pressed, full speed backward
                LBS = 255
                RBS = 255
                LFS = 0
                RFS = 0
                pi.set_PWM_dutycycle(PinLF, LFS)
                pi.set_PWM_dutycycle(PinLB, LBS)
                pi.set_PWM_dutycycle(PinRF, RFS)
                pi.set_PWM_dutycycle(PinRB, RBS)
                fontObj = pygame.font.Font('freesansbold.ttf' , 32)
                textSurfaceObj = fontObj.render('-255' + '     -255' , True, WHITE)
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (200, 150)
                DISPLAYSURF.blit(textSurfaceObj, textRectObj)
                pygame.display.update()
            if (event.key == K_a): # A key pressed, rotate right, wheels are in opposite directions
                LBS = 255
                RBS = 0
                LFS = 0
                RFS = 255
                pi.set_PWM_dutycycle(PinLF, LFS)
                pi.set_PWM_dutycycle(PinLB, LBS)
                pi.set_PWM_dutycycle(PinRF, RFS)
                pi.set_PWM_dutycycle(PinRB, RBS)
                fontObj = pygame.font.Font('freesansbold.ttf' , 32)
                textSurfaceObj = fontObj.render('-255' + '     255' , True, WHITE)
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (200, 150)
                DISPLAYSURF.blit(textSurfaceObj, textRectObj)
                pygame.display.update()
            if (event.key == K_d): # D key pressed, rotate right, wheels are in opposite directions
                LBS = 0
                RBS = 255
                LFS = 255
                RFS = 0
                pi.set_PWM_dutycycle(PinLF, LFS)
                pi.set_PWM_dutycycle(PinLB, LBS)
                pi.set_PWM_dutycycle(PinRF, RFS)
                pi.set_PWM_dutycycle(PinRB, RBS)
                fontObj = pygame.font.Font('freesansbold.ttf' , 32)
                textSurfaceObj = fontObj.render('255' + '     -255' , True, WHITE)
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (200, 150)
                DISPLAYSURF.blit(textSurfaceObj, textRectObj)
                pygame.display.update()
            if (event.key == K_SPACE): # Space key pressed, stop/brake, zeros on all GPIO pins
                LBS = 0
                RBS = 0
                LFS = 0
                RFS = 0
                pi.set_PWM_dutycycle(PinLF, LFS)
                pi.set_PWM_dutycycle(PinLB, LBS)
                pi.set_PWM_dutycycle(PinRF, RFS)
                pi.set_PWM_dutycycle(PinRB, RBS)
                fontObj = pygame.font.Font('freesansbold.ttf' , 32)
                textSurfaceObj = fontObj.render('0' + '     0' , True, WHITE)
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (200, 150)
                DISPLAYSURF.blit(textSurfaceObj, textRectObj)
                pygame.display.update()
        

        

