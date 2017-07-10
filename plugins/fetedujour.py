from json import JSONDecodeError
from urllib.error import URLError
from urllib.request import urlopen, Request
import re
import utils

def instance():
    return Fetedujour()

class Fetedujour(object):
    def __init__(self):
        self.url = "http://fetedujour.fr/"

    def go(self):
        if not utils.internet_reachable():
            print("FeteDuJour : Offline")
            return -1
        try:
            req = Request(self.url,None,{'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
            resp = urlopen(req)
            content = resp.read()
            data = re.search(r"<section class=\"bg\">.*?:(.*?)<\/h2>",str(content))
            if(data):
                print('[FDJ] Today we are celebrating : '+data.group(1).strip())
            else:
                print("No match found")

        except URLError as e:
            print("[FDJ] Mango goes out of the plate !")
            print("Error while downloading data ("+str(e)+")")

        except JSONDecodeError as e:
            print("[FDJ] Mango can't parse data :(")

