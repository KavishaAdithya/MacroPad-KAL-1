import json
import serial
import asyncio
import threading
import webbrowser
import http.server
import socketserver
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume

PORT = 8000

handler = http.server.SimpleHTTPRequestHandler

devices = AudioUtilities.GetSpeakers()

interface = devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)

volume = cast(interface,POINTER(IAudioEndpointVolume))

channel = None
past_Vol = volume.GetMasterVolumeLevelScalar()
past_Vol = round(past_Vol * 100)


def start_server():
    with socketserver.TCPServer(("",PORT),handler) as httpd:
        print(f"Serving at Port:{PORT}")
        httpd.serve_forever()

def setup_serial():

    global channel
    if channel is None:
        try:
            channel = serial.Serial("COM4",timeout=0.1,write_timeout=2)
            
        except Exception as ex:
            print(ex)
            channel = None
    return channel


async def read_Serial():
    
    setup_serial()
    line = None
    try:
        line = channel.readline()
    except KeyboardInterrupt:
        print("Keyboard - Interrupt")
        exit()

    except:
        await asyncio.sleep(1)
        return None
    
    data = {}
    if line != b"":
        try:
            data = json.loads(line.decode("utf-8"))
            print(data)
        except:
            data = {"raw": line.decode("utf-8")}
            print(data)
            
    if "Key" in data:
        if data["Key"] == "2":
            webbrowser.open(f"http://localhost:{PORT}/Macropad KAL/Voice Search.html")
        if data["Key"] == "6":
            webbrowser.open("https://www.google.com")
    
    await asyncio.sleep(0.1)


async def read_Vol():

    
    setup_serial()
    current_volume = volume.GetMasterVolumeLevelScalar()
    vol = str(round(current_volume * 100))
    return json.dumps({"VOL":vol,"script":1})


async def send_Data():
    
    setup_serial()
    
    data_out = await read_Vol()
    

    if data_out:
        try:
            channel.write((data_out + "\r\n").encode('utf-8'))
            
        except Exception as e:
            print(e)
    await asyncio.sleep(0.1)

async def main():

    global past_Vol
    current_volume = volume.GetMasterVolumeLevelScalar()
    vol = round(current_volume * 100)

    if vol != past_Vol:   
        await send_Data()
        past_Vol = vol

    await read_Serial()


if __name__ == "__main__":

    server_thread = threading.Thread(target = start_server,daemon=True)
    server_thread.start()

    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print("Err",e)
    
