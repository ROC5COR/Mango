import json
import os
import inspect
from http.client import RemoteDisconnected
from urllib.error import URLError
from urllib.request import urlopen
import mango


def loadJSON(file_name):
    # print('Load file : '+file_name)
    file = open(file_name)
    data = json.loads(file.read())
    return data



def getMangoFolder():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def getAbsoluteFilePath(filename: str):
    return os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), filename)


def getPluginsPath():
    return os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), mango.get_plugins_folder())


def getConfigFile(file_name):
    global config_path
    return os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), mango.get_config_folder(), file_name)



def internet_reachable():
    google_server = 'http://216.58.192.142'
    try:
        urlopen(google_server, timeout=4)
        return True
    except URLError:
        return False
    except RemoteDisconnected:
        return False
    except ConnectionResetError:
        return False


