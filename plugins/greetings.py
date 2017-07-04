import random
import time

import utils

def instance():
    return Greetings()

class Greetings(object):
    def __init__(self):
        data = utils.loadJSON(utils.getConfigFile('greetings.json'))
        user_name = data['user_name']
        self.morningGreetings = ['Bonjour '+user_name+', bonne journée !', 'Bonjour, bon matin !']
        self.middayGreetings = ['Bonjour :)', 'Hola !','Salut !', 'Salut ! :)','Yo !']
        self.eveningGreetings = ['Bonsoir !','Bonne soirée à vous', 'Bonsoir '+user_name+' !']

    def go(self):
        currentHour = int(time.localtime().tm_hour)
        if currentHour <= 11:
            print('[GRTNGS] '+random.choice(self.morningGreetings))
        elif 11 < currentHour <= 18:
            print('[GRTNGS] '+random.choice(self.middayGreetings))
        elif currentHour > 18:
            print('[GRTNGS] '+random.choice(self.eveningGreetings))
        else:
            print("Can say hello to mango !")


