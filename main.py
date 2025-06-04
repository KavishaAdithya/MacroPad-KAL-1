import serial
import bluetooth
import webbrowser
import os


url = ""
ser = serial.Serial('COM13',115200)

while True:
    line = ser.readline().decode('utf-8').strip()
    print(line)

    if line == "Key2":
        file_path = os.path.abspath("Voice Search.html")
        webbrowser.open(f"file://{file_path}")

    elif line == "Key5":
        nearby_devices = bluetooth.discover_devices(duration=5,lookup_names=True,flush_cache=True,lookup_class=True)
        print("Found {} devices".format(len(nearby_devices)))

        for addr, name,_ in nearby_devices:
            try:
                print("   {} - {}".format(addr, name))

                addr, name,_ = nearby_devices[0]
                port =1

                try:
                    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                    sock.connect((addr,port))
                    print(f"Connected to {name}")

                except Exception as e:
                    print(e)

            except UnicodeEncodeError:
                print("   {} - {}".format(addr, name.encode("utf-8", "replace")))

    elif line == "Key6":
        webbrowser.open("https://www.google.com")

