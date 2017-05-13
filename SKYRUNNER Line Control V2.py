# Program written by Joshua Koh (joshuakoh225@gmail.com) 
# for Fallon Middle School, Dublin, CA
import time
import pygame
import sys
import curses
import atexit
import pigpio

from pygame.locals import *

pi = pigpio.pi()

outputList = [1, 0, 0] #3 bytes for MCP3008
sampled_list = [0, 0, 0, 0, 0, 0, 0, 0]
LINE_DETECT = [0, 0, 0, 0, 0, 0, 0, 0]
ThresholdCount = 621 #Threshold for sensing line
spi_flags = 3 #works for MCP3008
h = pi.spi_open(0, 1000000, spi_flags)
threshold = 1.95

def lineSensor (h, threshold,lineOut):
    c = 0
    secondElm = 0
    outputList = [1, secondElm, 0]
    LED_STATE = 0
    sampled_list = [0, 0, 0, 0, 0, 0, 0, 0]
    while c < 8:
        #secondElm = 128 + c
        outputList[1] = 128 + c*16
        #print (outputList)
        #(count, rx_data) = pi.spi_xfer(h,outputList)    
        #time.sleep(0.001)
        (count, rx_data) = pi.spi_xfer(h,outputList)
        #print("count is " + str(count))
        #print("tuple is " + str(rx_data[0]) + " " + str(rx_data[1]) + " " + str(rx_data[2]))
        sampled_list[c] = (rx_data[1]<<8) + rx_data[2]
        #print("sampled voltage is " + str(sampled_list[c]*3.3/1024))
        #print()
##        if LED_STATE == 0:
##            pi.write(BLINK_PIN_OUTPUT, 1)
##            LED_STATE = 1
##        elif LED_STATE == 1:
##            pi.write(BLINK_PIN_OUTPUT, 0)
##            LED_STATE = 0
        sampled_list[c]= round(sampled_list[c]*3.3/1024,2)

        if lineOut:
            if sampled_list[c] > threshold:
                sampled_list[c] = 1
            elif sampled_list[c] <= threshold:
                sampled_list[c] = 0
                
        c +=  1

    return(sampled_list)

print("____________________________________________")
print("Welcome to the FEL Automatic Car Control!")
print()
print("INSTRUCTIONS:")
print("This car will follow a 3/4 inch line. There is no manual control.")
print("Have fun!")
print("________________________________________")
print()
input("Press <Enter> to Continue.")

#pygame.init()
#DISPLAYSURF = pygame.display.set_mode((400, 300))

##WHITE = (255, 255, 255)
##BLACK = (  0,   0,   0)
##BLUE  = (  0,   0, 255)

ButtonPin = 4 #Different from Josh, Emergency Stop 
ButtonPinState = 0

PIN_1 = 18
PIN_2 = 24
PIN_3 = 17
PIN_4 = 22

BLINK_PIN_OUTPUT = 12

AVG_LISTRIGHT = [0, 0, 0, 0]
AVG_LISTLEFT = [0, 0, 0, 0]

LED_STATE = 0

DiffSPD = 0 #Differential Speed btw left and right wheels
AvgVar = 155 #Average PWM counts for motor
MaxVar = 255 #Max PWM counts for motor
MinVar = 0 #Min PWN counts for motor
Kp = 30 #Proportional gain
totalnowright = 0
totalnowleft = 0
oldestright = 0
oldestleft = 0
m = 0
p = 0
fourtime = 2
right = 0
left = 0

SMULSPD = 255 #Rwheel
SMULSPD2 = 255 #Lwheel

PIN_SPD = AvgVar #Rwheel
PIN_SPD2 = AvgVar #Lwheel
pi.set_mode(BLINK_PIN_OUTPUT, pigpio.OUTPUT) 
#pi.set_mode(BLINK_PIN_INPUT, pigpio.INPUT)

##pi.set_mode(LED_1, pigpio.OUTPUT)##LED to display line sensor status
##pi.set_mode(LED_2, pigpio.OUTPUT)
##pi.set_mode(LED_3, pigpio.OUTPUT)
##pi.set_mode(LED_4, pigpio.OUTPUT)
##pi.set_mode(LED_5, pigpio.OUTPUT)
##pi.set_mode(LED_6, pigpio.OUTPUT)
##

pi.set_mode(PIN_1, pigpio.OUTPUT) #Motor pins 1-4
pi.set_mode(PIN_2, pigpio.OUTPUT) 
pi.set_mode(PIN_3, pigpio.OUTPUT) 
pi.set_mode(PIN_4, pigpio.OUTPUT) 
pi.set_mode(BLINK_PIN_OUTPUT, pigpio.OUTPUT) 

pi.set_mode(ButtonPin, pigpio.INPUT)
pi.set_pull_up_down(ButtonPin, pigpio.PUD_UP)

pi.set_PWM_dutycycle(PIN_1, MinVar) #Right Forward PWM
pi.set_PWM_dutycycle(PIN_3, MinVar) #Left Forward PWM
pi.set_PWM_dutycycle(PIN_2, 0) #Right Backwards PWM
pi.set_PWM_dutycycle(PIN_4, 0) #Left Backwards PWM


#try:
while True:
    
        LINE_DETECT = lineSensor(h,threshold, True)

        #Form RightError and LeftError for directional control
        RightError = LINE_DETECT[2] + (LINE_DETECT[1] * 3.)
        LeftError = LINE_DETECT[5] + (LINE_DETECT[6]  * 3.)

        #If block below is not active or disabled by setting fourtime = 2
        if fourtime < 2: # running average implementation
            AVG_LISTRIGHT[m] = RightError # using sum and oldest
            AVG_LISTLEFT[m] = LeftError
            totalnowright += RightError
            totalnowleft += LeftError
            fourtime += 1 
            oldestright = AVG_LISTRIGHT[0] #First time only
            oldestleft = AVG_LISTLEFT[0]
            m += 1
        else:
            right = RightError #totalnowright/4 
            left = LeftError #totalnowleft/4
            #print("Right: " + str(right) + "    Left: " + str(left))
            m = m%2
            AVG_LISTRIGHT[m] = RightError
            AVG_LISTLEFT[m] = LeftError
            totalnowright = totalnowright - oldestright + RightError
            oldestright = AVG_LISTRIGHT[(m+1) %2]
            totalnowleft = totalnowleft - oldestleft + LeftError
            oldestleft = AVG_LISTLEFT[(m+1) %2]
            m += 1
                  
            if right > 0: # there is non zero error at the right
                DiffSPD = Kp * right
                PIN_SPD = AvgVar - int(DiffSPD) # Right Wheel
                PIN_SPD2 = AvgVar + int(DiffSPD*2) # Left Wheel
                

            if left > 0:
                DiffSPD = Kp * left
                PIN_SPD = AvgVar + int(DiffSPD*2)# Right Wheel
                PIN_SPD2 = AvgVar - int(DiffSPD) # Left Wheel
              
            # make sure PWM is not going negative or over max 255
            if PIN_SPD <= MinVar:
                PIN_SPD = MinVar + 1
            elif PIN_SPD > MaxVar:
                PIN_SPD = MaxVar

            if PIN_SPD2 <= MinVar:
                PIN_SPD2 = MinVar + 1
            elif PIN_SPD2 > MaxVar:
                PIN_SPD2 = MaxVar

            #This is a print statement for debugging the sensor output
            #print(LINE_DETECT)
            #print("R: " + str(right) + "    L: " + str(left) + "    PIN_SPD: " + str(PIN_SPD) + "    PIN_SPD2:" + str(PIN_SPD2) + "    DiffSPD:" + str(DiffSPD))
            pi.set_PWM_dutycycle(PIN_1, PIN_SPD) # Right Wheel
            pi.set_PWM_dutycycle(PIN_3, PIN_SPD2) #Left Wheel


        #Turns off motors when  button is pressed
        ButtonPinState = pi.read(ButtonPin)
        if ButtonPinState == 0:
            PIN1_SPD = 0
            PIN2_SPD = 0
            pi.set_PWM_dutycycle(PIN_1, PIN1_SPD)
            pi.set_PWM_dutycycle(PIN_2, PIN2_SPD)
            pi.set_PWM_dutycycle(PIN_3, PIN1_SPD)
            pi.set_PWM_dutycycle(PIN_4, PIN2_SPD)
            break
pi.stop()
pi.spi_close(h)
print("Terminating Program...")
time.sleep(1)
print("Done.")
