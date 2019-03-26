import serial
from serial.tools.list_ports import  comports
import time
import sys
from Plugin import Plugin
from MessageListener import MessageListener

def instance():
    return Uart()


class Uart(Plugin):
    def __init__(self):
        self.serial = None
        self.portToChoose = -1
        self.ports = []
        self.baudrate = 9600

    def normalize_text(self, text):

        return str(text.decode('UTF-8'))

    def enumerate_ports(self, message_listener):
        self.ports.clear()
        for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
            message_listener.printMessage('> {:2}: {:20} {}\n'.format(n, port, desc))
            self.ports.append(port)

    def open_port(self, message_listener):
        self.enumerate_ports(message_listener=message_listener) # TODO : to change by a static variables shared by each instance of this class

        if len(self.ports) <= 0:
            message_listener.printMessage("No port to open ("+str(len(self.ports))+" ports available")
            return -1
        if self.portToChoose > len(self.ports) and self.portToChoose != -1:
            message_listener.printMessage("Wrong port choice (port number : "+str(self.portToChoose)+")")
            return -1
        try:
            self.serial = serial.Serial(self.ports[self.portToChoose], timeout=1)
            message_listener.printMessage('Opening port : '+self.ports[self.portToChoose])
        except OSError as e:
            message_listener.printMessage("Error: can't open port: "+str(e))

        try:
            while(True):
                try:
                    data = self.serial.read(self.serial.in_waiting or 1)

                    if data:
                        sys.stdout.write(self.normalize_text(data))
                        sys.stdout.flush()
                    time.sleep(0.01)
                except UnicodeDecodeError as e:
                    message_listener.printMessage("[UART] Error : "+str(e))
        except KeyboardInterrupt:
            message_listener.printMessage("Closing connection")
            self.serial.close()

    def go(self, args: list, message_listener: MessageListener = MessageListener()):
        if len(args) == 0:
            self.enumerate_ports(message_listener=message_listener)
            message_listener.printMessage("Syntax :\n- uart list\n- uart connect [port_number] [baudrate]")
        elif args[0] == "list":
            self.enumerate_ports(message_listener=message_listener)
        elif args[0] == "help":
            message_listener.printMessage("Syntax :\n- uart list\n- uart connect [port_number] [baudrate]")
        elif args[0] == "connect":
            if len(args) == 3:
                self.baudrate = int(args[2])
                self.portToChoose = int(args[1])
                self.open_port(message_listener=message_listener)
            elif len(args) == 2:
                self.portToChoose = int(args[1])
                self.open_port(message_listener=message_listener)
            elif len(args) == 1:
                self.portToChoose = len(args) - 1
                self.open_port(message_listener=message_listener)
            else:
                message_listener.printMessage("Syntax error")
        else:
            message_listener.printMessage("Command "+str(args[0])+" unknown")