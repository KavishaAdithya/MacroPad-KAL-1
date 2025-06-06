# On PC (Python)
import serial

ser = serial.Serial('COM13', baudrate=115200)  # Use appropriate port
ser.write(b"Hello RP2040\n")

response = ser.readline().decode().strip()
print(response)