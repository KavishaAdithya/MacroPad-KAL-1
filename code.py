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
import json
import TEST


usb_cdc.data.timeout = 0.1


encoder_Button = DigitalInOut(board.GP19)
encoder_Button.direction = Direction.INPUT
encoder_Button.pull = Pull.UP

onboard_led = DigitalInOut(board.LED)
onboard_led.direction = Direction.OUTPUT

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


while True:
    
    data_out = {}
    data_rec = None
    
    if usb_cdc.data.in_waiting >0:
        data_in = usb_cdc.data.readline()
        
        if len(data_in)>0:
            try:
                data_rec = json.loads(data_in)
                print(data_rec)
            except ValueError:
                data_rec = {"raw":data_in.decode()}
                
    position = encoder.position

    if position != last_Position or last_Position == None:
        #print(position,last_Position)
        #display.fill(0)
        #OLED_Disp(f"{position}",10,10,255, size=2)
        #Send_Data("VOL\n")
        
                #TEST.display_Header(pc=True,mic=False,speaker_mute=False,speaker_unmute=True,text1=data_rec)
                    
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
            
            if key == '1':
                open_Links("https://www.youtube.com/")        
                
            elif key == '2':
                data_out = {"Key":"2"}
                      
            elif key == '3':
                open_Links("https://chatgpt.com/")                
                
            elif key == '4':
                open_Links("https://lms.eng.sjp.ac.lk/")
                               
            elif key == '5':
                ConsuB.send(ConsumerControlCode.PLAY_PAUSE)
                                
            elif key == '6':
                data_out = {"Key":"6"}
                               
            elif key == '7':
                keyB.send(Keycode.WINDOWS,Keycode.LEFT_SHIFT,Keycode.S)
                               
            elif key == '8':
                keyB.send(Keycode.WINDOWS,Keycode.D)
                               
            elif key == '9':
                open_Links("https://github.com/")
                
            if data_out:
                print(json.dumps(data_out))
                usb_cdc.data.write(json.dumps(data_out).encode("utf-8")+b"\r\n")
                
        elif event.released:
            None
            
            
    
        
        
            

