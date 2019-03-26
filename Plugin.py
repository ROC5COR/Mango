from MessageListener import MessageListener
from enum import Enum

class Period(Enum):
    NEVER = "NEVER"
    HOURLY = "HOURLY"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"

class Plugin():
    def go(self, args:list, message_listener:MessageListener = MessageListener()):
        print("Default go method")

    def get_aliases(self):
        return []

    def update(self):
        None

    def get_update_period(self):
        return [{'time':None,'repeat':Period.NEVER}] # 'time' : [Hour,Minutes], 'repeat':Period
