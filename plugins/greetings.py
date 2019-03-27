import random
import time
from Plugin import Plugin
import utils
from MessageListener import MessageListener
from ParameterManager import ParamameterManager


def instance():
    return Greetings()

class Greetings(Plugin):
    def __init__(self):
        pm = ParamameterManager(self.__class__, 'config.json')

        #data = utils.loadJSON(utils.getConfigFile('greetings.json'))
        #user_name = data['user_name']
        user_name = pm.get_param('user_identity', '')
        self.morningGreetings = ['Bonjour '+user_name+', bonne journée !', 'Bonjour, bon matin !']
        self.middayGreetings = ['Bonjour :)', 'Hola !','Salut !', 'Salut ! :)','Yo !']
        self.eveningGreetings = ['Bonsoir !','Bonne soirée à vous', 'Bonsoir '+user_name+' !']

    def go(self, args: list, message_listener: MessageListener = MessageListener()):
        currentHour = int(time.localtime().tm_hour)
        if currentHour <= 11:
            message_listener.printMessage('[GRTNGS] '+random.choice(self.morningGreetings))
        elif 11 < currentHour <= 18:
            message_listener.printMessage('[GRTNGS] '+random.choice(self.middayGreetings))
        elif currentHour > 18:
            message_listener.printMessage('[GRTNGS] '+random.choice(self.eveningGreetings))
        else:
            message_listener.printMessage("Can say hello to mango !")


