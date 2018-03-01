from json import JSONDecodeError
from urllib.error import URLError
import googlefinance as gf
import json
from prettytable import PrettyTable
import time
import utils


def instance():
    return Finance()


class Finance(object):
    def __init__(self):
        self.values = []
        values = utils.loadJSON(utils.getConfigFile('finance.json'))['values']
        #for value in values:
            #self.values.append(value)
        #self.table = PrettyTable(['Name', 'LstTrdPrice', 'LstTrdTime'])

    def go(self, args):
        print("[FNC]")
        print("[FNC] Financial module unavailable")
        return -1

        thereIsData = False

        if not utils.internet_reachable():
            print("Finance : Offline")
            return -1

        for value in self.values:
            try:
                rawData = str(gf.getQuotes(value)).replace("'", '"')
                jData = json.loads(rawData)[0]
                self.table.add_row([value, jData['LastTradePrice'], jData['LastTradeTime']])
                thereIsData = True
            except URLError as e:
                print("Error while downloading data(" + str(e) + ")")
            except JSONDecodeError as e:
                print("Error while parsing data")

        if thereIsData == True:
            print(self.table)
        else:
            print("No data")
