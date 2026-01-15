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

profile_num = 0

km = keypad.KeyMatrix(row_pins=rows,column_pins=cols,columns_to_anodes=False,interval=0.01)

def open_Links(url):
    keyB.send(Keycode.WINDOWS,Keycode.R)
    time.sleep(0.5)
    Keyboard_Layout.write(url)
    keyB.send(Keycode.ENTER)
    
    
def open_Apps(name):
    keyB.send(Keycode.WINDOWS)
    time.sleep(0.5)
    Keyboard_Layout.write(name)
    keyB.send(Keycode.ENTER)
    
    
    
profile_0_actions ={
    
    "1":lambda:open_Links("https://www.youtube.com/"),
    "2":lambda:open_Links("https://aistudio.google.com/prompts/new_chat"),
    "3":lambda:open_Links("https://lms.eng.sjp.ac.lk/"),
    "4":lambda:open_Links("https://github.com/"),
    "5":lambda:open_Links("https://play.hbomax.com/"),
    "6":lambda:open_Links("https://mail.google.com/mail/u/0/#inbox"),
    "7":lambda:open_Apps("Netflix"),
    "8":lambda:open_Apps("Whatsapp")
    
    }

profile_1_actions ={
    
    "1":lambda:ConsuB.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK),
    "4":lambda:ConsuB.send(ConsumerControlCode.STOP),
    "7":lambda:ConsuB.send(ConsumerControlCode.SCAN_NEXT_TRACK),
    "2":lambda:keyB.send(Keycode.LEFT_ARROW),
    "5":lambda:ConsuB.send(ConsumerControlCode.PLAY_PAUSE),
    "8":lambda:keyB.send(Keycode.RIGHT_ARROW),
    "3":lambda:None,
    "6":lambda:None
    
    }


profile_2_actions ={
    
    "1":lambda:keyB.send(Keycode.LEFT_CONTROL,Keycode.A), #Select ALL
    "4":lambda:keyB.send(Keycode.LEFT_CONTROL,Keycode.Z), #Undo
    "7":lambda:keyB.send(Keycode.LEFT_CONTROL,Keycode.Y), #Redo
    "2":lambda:keyB.send(Keycode.LEFT_ALT,Keycode.EQUALS), #insert equation
    "5":lambda:keyB.send(Keycode.LEFT_CONTROL,Keycode.LEFT_SHIFT,Keycode.EQUALS), #insert superscript
    "8":lambda:keyB.send(Keycode.LEFT_CONTROL,Keycode.LEFT_SHIFT,Keycode.MINUS), #insert subscript
    "3":lambda:None,
    "6":lambda:None
    
    }

profiles = [
    profile_0_actions,
    profile_1_actions,
    profile_2_actions
    ]

box = [["YT","Git","Netf","AI","HBO","Whts","LMS","Gmail",">>"],
       [" < |"," Stop"," | >","  <"," > ||","  >","test2","test2"," >>"],
       ["Sel","Undo","Redo","Eqn","Sup","Sub","test3","test3"," >>"]]


TEST.key_bindings(box[0])


while True:
        
    position = encoder.position
   
    if position != last_Position or last_Position == None:
                    
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
                    
                if key == "9":
                     profile_num=profile_num+1
                     profile_num = profile_num%3
                     TEST.key_bindings(box[profile_num])
                     print(profile_num)
                     
                else:
                    current_profile = profiles[profile_num]
                    if key in current_profile:
                        current_profile[key]()
                                    
        elif event.released:
            None
            
            
    
        
        
            

