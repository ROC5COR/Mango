import mango
import os
from Plugin import Plugin
from MessageListener import MessageListener

def instance():
    return Help()

class Help(Plugin):

    def go(self, args: list, message_listener: MessageListener = MessageListener()):
        message_listener.printMessage("Modules present :")

        raw_file_list = os.listdir(mango.get_plugins_path())

        for raw_file in raw_file_list:
            if raw_file.endswith('.py'):
                message_listener.printMessage("\t- "+str(raw_file[:-3]))

    def get_aliases(self):
        return ['h']
