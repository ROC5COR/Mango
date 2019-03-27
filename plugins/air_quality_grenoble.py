from json import JSONDecodeError
from urllib.error import URLError
from urllib.request import urlopen, Request
import re
import utils
import ssl
from Plugin import Plugin
from MessageListener import MessageListener
from Value import Value

def instance():
    return AirQualityGrenoble()

class AirQualityGrenoble(Plugin):
    def __init__(self):
        self.url = "https://www.atmo-auvergnerhonealpes.fr/monair/commune/38185"

    def go(self, args: list, message_listener: MessageListener = MessageListener()):
        if not utils.internet_reachable():
            message_listener.printMessage("AirQualityGrenoble : Offline")
            return -1
        try:
            req = Request(self.url,None,{'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
            gcontext = ssl.SSLContext()
            resp = urlopen(req, context=gcontext) # Do not use with critical data
            content = resp.read()
            data = re.search(r"<div.*class=\"indice\">(\d*)<\/div>",str(content))
            if(data):
                val = Value(data.group(1).strip(), 
                    data_type='int', data_unit=None, data_description='air quality',
                    associated_string='Today air quality in Grenoble is : {} (0 is the best, 100 is the worst)')
                #message_listener.printMessage('[AQG] Today air quality in Grenoble is : '+data.group(1).strip())
                message_listener.printValue(val)
            else:
                message_listener.printMessage("No match found")

        except URLError as e:
            message_listener.printMessage("Error while downloading data ("+str(e)+")")

        except JSONDecodeError as e:
            message_listener.printMessage("[AQG] Mango can't parse data :(")

    def get_aliases(self):
        return ['air']
