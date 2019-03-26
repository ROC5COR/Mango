import threading

from MessageListener import MessageListener

class ClientConnection(threading.Thread, MessageListener):

    def __init__(self, ip, port, clientsocket, instance):
        threading.Thread.__init__(self)
        self.instance = instance
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] New thread for %s %s" % (self.ip, self.port,))
        

    def run(self):

        try:
            print("New client connected %s %s" % (self.ip, self.port))
            while True:
                r = self.clientsocket.recv(2048)
                if r.decode('utf-8') != "":
                    print("["+str(self.ip)+"]:", r)
                    self.instance.parse_command(r.decode('utf-8').strip().split(' '), message_listener=self)
                    #self.printMessage("Ok\n")#To check connection
        except ConnectionError:
            print("Client disconnected")
        finally:
            self.clientsocket.close()


    def printMessage(self, message:str):
        print("[->]"+message)
        self.clientsocket.send(message.encode('utf-8'))