from json import JSONDecodeError
from urllib.error import URLError
import googlefinance as gf
import json
from prettytable import PrettyTable
import time
import utils

def instance():
	return finance()

class finance():
    def __init__(self):
        self.values = []
        values = utils.loadJSON(utils.getMangoPath() + '/config/finance.json')['values']
        for value in values:
            self.values.append(value)
        self.table = PrettyTable(['Name', 'LstTrdPrice', 'LstTrdTime'])

    def go(self):
        print("[FNC]")
        t = time.localtime()
        # print("Current time : "+str(t.tm_hour)+"h"+str(t.tm_min))
        thereIsData = False
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
