import serial
from serial.tools.list_ports import  comports
import time
import sys
import os

def instance():
    return Uart()

class Uart(object):
    def __init__(self):
        self.serial = None
        self.portToChoose = -1
        self.ports = []

    def normalize_text(self, text):

        return str(text.decode('UTF-8'))

    def enumerate_ports(self):
        self.ports.clear()
        for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
            print('> {:2}: {:20} {}'.format(n, port, desc))
            self.ports.append(port)

    def open_port(self):
        if len(self.ports) <= 0:
            print("No port to open")
            return
        if self.portToChoose < len(self.ports) and self.portToChoose != -1:
            print("Wrong port choice")
            return
        self.serial = serial.Serial(self.ports[self.portToChoose], timeout=1)
        print('Opening port : '+self.ports[self.portToChoose])

        try:
            while(True):
                data = self.serial.read(self.serial.in_waiting or 1)

                if data:
                    sys.stdout.write(self.normalize_text(data))
                    sys.stdout.flush()
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("Closing connection")
            self.serial.close()

    def go(self):
        self.enumerate_ports()
        if len(self.ports) > 0:
            self.open_port()
        else:
            print("No com ports detected")

