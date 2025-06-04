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
import sys

encoder_Button = DigitalInOut(board.GP19)
encoder_Button.direction = Direction.INPUT
encoder_Button.pull = Pull.UP


rows = (board.GP6,board.GP7,board.GP8)
cols = (board.GP3,board.GP4,board.GP5)

keyB = Keyboard(usb_hid.devices)
Keyboard_Layout = KeyboardLayoutUS(keyB)

ConsuB = ConsumerControl(usb_hid.devices)

encoder = rotaryio.IncrementalEncoder(board.GP20,board.GP21)

last_Position = None

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
    

while True:
   
    position = encoder.position
    if last_Position == None or position != last_Position:
        print(position)
        if last_Position != None:
            
            try:
                if position > last_Position:
                    ConsuB.send(ConsumerControlCode.VOLUME_INCREMENT)
                elif position < last_Position:
                    ConsuB.send(ConsumerControlCode.VOLUME_DECREMENT)
                    
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
            print("Pressed:", key)
            if key == '1':
                open_Links("https://www.youtube.com/")
                
            elif key == '2':
                sys.stdout.write("Key2\n")
                time.sleep(2)
  
            elif key == '3':
                open_Links("https://chatgpt.com/")
                
            elif key == '4':
                open_Links("https://lms.eng.sjp.ac.lk/")
                
            elif key == '5':
                ConsuB.send(ConsumerControlCode.PLAY_PAUSE)
                
            elif key == '6':
                sys.stdout.write("Key6\n")
                time.sleep(2)
                
            elif key == '7':
                keyB.send(Keycode.WINDOWS,Keycode.LEFT_SHIFT,Keycode.S)
                
            elif key == '8':
                keyB.send(Keycode.WINDOWS,Keycode.D)
                
            elif key == '9':
                open_Links("https://github.com/")

                        
        elif event.released:
            print("Released:", key)
            
            
    
        
        
            
