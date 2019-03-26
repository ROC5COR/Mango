from MessageListener import MessageListener

class CommandLineInterface(MessageListener): # Maybe inherited from a common interface with NetworkInterface
    def __init__(self):
        self.command_line_message = "[CLI]>"
    
    def wait_for_input(self):
        return input(self.command_line_message)

    def printMessage(self, message):
        print(message)

