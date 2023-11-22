import serial
import time

class Esp:
    def __init__(self):
        self.e = serial.Serial(port='COM4', baudrate=9600, timeout=2)
        time.sleep(2)

# Create an instance of the Esp class
#esp_instance = Esp()
