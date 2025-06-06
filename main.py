import serial
import webbrowser
import os
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()

interface = devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)

volume = cast(interface,POINTER(IAudioEndpointVolume))

current_volume = volume.GetMasterVolumeLevelScalar()

ser = serial.Serial('COM13',115200)

while True:
    line = ser.readline().decode('utf-8').strip()
    print(line)

    if line == "Key2":
        file_path = os.path.abspath("Voice Search.html")
        webbrowser.open(f"file://{file_path}")

    elif line == "Key6":
        webbrowser.open("https://www.google.com")

    current_volume = volume.GetMasterVolumeLevelScalar()
    vol = str(round(current_volume * 100))
    ser.write(f"vol{vol}\n".encode())
       
       

    
