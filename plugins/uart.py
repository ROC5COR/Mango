import serial
from serial.tools.list_ports import  comports
import time
import sys
from mango_plugin import mango_plugin

def instance():
    return Uart()


class Uart(mango_plugin):
    def __init__(self):
        self.serial = None
        self.portToChoose = -1
        self.ports = []
        self.baudrate = 9600

    def normalize_text(self, text):

        return str(text.decode('UTF-8'))

    def enumerate_ports(self):
        self.ports.clear()
        for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
            print('> {:2}: {:20} {}'.format(n, port, desc))
            self.ports.append(port)

    def open_port(self):
        self.enumerate_ports() # TODO : to change by a static variables shared by each instance of this class

        if len(self.ports) <= 0:
            print("No port to open ("+str(len(self.ports))+" ports available")
            return -1
        if self.portToChoose > len(self.ports) and self.portToChoose != -1:
            print("Wrong port choice (port number : "+str(self.portToChoose)+")")
            return -1
        self.serial = serial.Serial(self.ports[self.portToChoose], timeout=1)
        print('Opening port : '+self.ports[self.portToChoose])

        try:
            while(True):
                try:
                    data = self.serial.read(self.serial.in_waiting or 1)

                    if data:
                        sys.stdout.write(self.normalize_text(data))
                        sys.stdout.flush()
                    time.sleep(0.01)
                except UnicodeDecodeError as e:
                    print("[UART] Error : "+str(e))
        except KeyboardInterrupt:
            print("Closing connection")
            self.serial.close()

    def go(self, args: list):
        if len(args) == 0:
            self.enumerate_ports()
            print("Syntax :\n- uart list\n- uart connect [port_number] [baudrate]")
        elif args[0] == "list":
            self.enumerate_ports()
        elif args[0] == "help":
            print("Syntax :\n- uart list\n- uart connect [port_number] [baudrate]")
        elif args[0] == "connect":
            if len(args) == 3:
                self.baudrate = int(args[2])
                self.portToChoose = int(args[1])
                self.open_port()
            elif len(args) == 2:
                self.portToChoose = int(args[1])
                self.open_port()
            elif len(args) == 1:
                self.portToChoose = len(args) - 1
                self.open_port()
            else:
                print("Syntax error")
        else:
            print("Command "+str(args[0])+" unknown")