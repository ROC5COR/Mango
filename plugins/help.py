import mango
import os
from mango_plugin import mango_plugin
from MessageListener import MessageListener

def instance():
    return Help()

class Help(mango_plugin):

    def go(self, args: list, message_listener: MessageListener = MessageListener()):
        message_listener.printMessage("Modules present :")

        raw_file_list = os.listdir(mango.plugins_path)

        for raw_file in raw_file_list:
            if raw_file.endswith('.py'):
                message_listener.printMessage("\t- "+str(raw_file[:-3])+"\n")

    def get_aliases(self):
        return ['h']