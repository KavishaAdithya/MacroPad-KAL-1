import usb_cdc


import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from digitalio import DigitalInOut,Direction,Pull
import time
import board
import keypad
import rotaryio

import busio
import adafruit_ssd1306

usb = usb_cdc.console
#print(usb)

encoder_Button = DigitalInOut(board.GP19)
encoder_Button.direction = Direction.INPUT
encoder_Button.pull = Pull.UP

i2c = busio.I2C(board.GP11,board.GP10)
display = adafruit_ssd1306.SSD1306_I2C(128,64,i2c)
display.fill(0)
display.show()
display.pixel(0,0,10)
display.pixel(64,16,10)
display.circle(64,16,5,255)

try:
    display.text("HELLO WORLD", 50, 32, 255,font_name='font5x8.bin', size=1)
except Exception as e:
    print(e)
    
display.show()
   
rows = (board.GP6,board.GP7,board.GP8)
cols = (board.GP3,board.GP4,board.GP5)

keyB = Keyboard(usb_hid.devices)
Keyboard_Layout = KeyboardLayoutUS(keyB)

ConsuB = ConsumerControl(usb_hid.devices)

encoder = rotaryio.IncrementalEncoder(board.GP20,board.GP21)

last_Position = None
position = 1

keys = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9']
]

km = keypad.KeyMatrix(row_pins=rows,column_pins=cols,columns_to_anodes=False,interval=0.01)

def open_Links(url):
    keyB.send(Keycode.WINDOWS,Keycode.R)
    time.sleep(0.5)
    Keyboard_Layout.write(url)
    keyB.send(Keycode.ENTER)
    
    
def OLED_VOL_Disp(VOL):
    display.fill(0)
    display.rect(10,10,100,10,255)
    display.rect(11,11,VOL,8,255,fill=True)
    
    display.show()

def Recieve_Data():
    #print(usb.in_waiting)
    if usb.in_waiting:
        command = usb.readline().decode().strip()
        return command

def OLED_Disp(Text,x,y,color,size):
    display.fill(0)
    display.text(Text,x,y,color,font_name='font5x8.bin',size=size)
    display.show()



while True:
   
    position = encoder.position
    if position != last_Position or last_Position == None:
        #print(position,last_Position)
        #display.fill(0)
        #OLED_Disp(f"{position}",10,10,255, size=2)
        #Send_Data("VOL\n")
        VOL = Recieve_Data()
                
        if last_Position != None:
            
            try:
                if position > last_Position:
                    ConsuB.send(ConsumerControlCode.VOLUME_INCREMENT)
                    #OLED_Disp(VOL,10,10,255, size=2)
                    OLED_VOL_Disp(int(VOL[3:]))
                    
                elif position < last_Position:
                    ConsuB.send(ConsumerControlCode.VOLUME_DECREMENT)
                    #OLED_Disp(VOL,10,10,255, size=2)
                    OLED_VOL_Disp(int(VOL[3:]))

                    
            except Exception as e:
                print(e)
        
        last_Position = position
    
    if not encoder_Button.value:
        ConsuB.send(ConsumerControlCode.MUTE)
  
    event = km.events.get()
    
    if event:
    
        row = event.key_number // len(cols)
        col = event.key_number % len(cols)
        key = keys[row][col]

        if event.pressed:
            
            if key == '1':
                open_Links("https://www.youtube.com/")
                
            elif key == '2':
                print("Key2\n")
                #time.sleep(2)
                
            elif key == '3':
                open_Links("https://chatgpt.com/")
                
            elif key == '4':
                open_Links("https://lms.eng.sjp.ac.lk/")
                
            elif key == '5':
                ConsuB.send(ConsumerControlCode.PLAY_PAUSE)
                
            elif key == '6':
                print("Key6\n")
                #time.sleep(2)
                
            elif key == '7':
                keyB.send(Keycode.WINDOWS,Keycode.LEFT_SHIFT,Keycode.S)
                
            elif key == '8':
                keyB.send(Keycode.WINDOWS,Keycode.D)
                
            elif key == '9':
                open_Links("https://github.com/")

                        
        elif event.released:
            display.fill(0)
            display.text(f"{key}",32,32,255,font_name='font5x8.bin', size=1)
            display.show()
            time.sleep(0.5)
            display.fill(0)
            display.show()
            
    
        
        
            
