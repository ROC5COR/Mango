from json import JSONDecodeError
from urllib.error import URLError
import googlefinance as gf
import json
from MessageListener import MessageListener
import utils
from mango_plugin import mango_plugin
from prettytable import PrettyTable

def instance():
    return Finance()


class Finance(mango_plugin):
    def __init__(self):
        self.values = []
        values = utils.loadJSON(utils.getConfigFile('finance.json'))['values']
        for value in values:
            self.values.append(value)
        self.table = PrettyTable(['Name', 'LstTrdPrice', 'LstTrdTime'])

    def go(self, args: list, message_listener: MessageListener = MessageListener()):
        message_listener.printMessage("[FNC]")
        message_listener.printMessage("[FNC] Financial module unavailable")
        return -1

        thereIsData = False

        if not utils.internet_reachable():
            message_listener.printMessage("Finance : Offline")
            return -1

        for value in self.values:
            try:
                rawData = str(gf.getQuotes(value)).replace("'", '"')
                jData = json.loads(rawData)[0]
                self.table.add_row([value, jData['LastTradePrice'], jData['LastTradeTime']])
                thereIsData = True
            except URLError as e:
                message_listener.printMessage("Error while downloading data(" + str(e) + ")")
            except JSONDecodeError as e:
                message_listener.printMessage("Error while parsing data")

        if thereIsData == True:
            message_listener.printMessage(self.table.get_string())
        else:
            message_listener.printMessage("No data")
