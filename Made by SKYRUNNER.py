import time
import pygame
import sys
import curses
import atexit
import pigpio

from pygame.locals import *
pi = pigpio.pi()

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
BLUE  = (  0,   0, 255)

PinLF = 24
PinLB = 18
PinRF = 22
PinRB = 17

pi.set_mode(PinLF, pigpio.OUTPUT)
pi.set_mode(PinLB, pigpio.OUTPUT)
pi.set_mode(PinRF, pigpio.OUTPUT)
pi.set_mode(PinRB, pigpio.OUTPUT) 


LFS = 0
LBS = 0
RFS = 0
RBS = 0

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
            LBS = 0
            RBS = 0
            LFS = 0
            RFS = 0
            pi.set_PWM_dutycycle(PinLF, LFS)
            pi.set_PWM_dutycycle(PinLB, LBS)
            pi.set_PWM_dutycycle(PinRF, RFS)
            pi.set_PWM_dutycycle(PinRB, RBS)
            pygame.quit()
        if event.type == KEYDOWN:
            if (event.key == K_w):
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
            if (event.key == K_s):
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
            if (event.key == K_a):
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
            if (event.key == K_d):
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
            if (event.key == K_SPACE):
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
        

        

