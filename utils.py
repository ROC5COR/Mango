import sys
import json
import os
import inspect
from http.client import RemoteDisconnected
from importlib import import_module
from urllib.error import URLError
from urllib.request import urlopen
from distutils.version import StrictVersion

configPath = "home_config" # default value

mango_version = StrictVersion('0.1.1')

def loadJSON(file_name):
    #print('Load file : '+file_name)
    file = open(file_name)
    data = json.loads(file.read())
    return data


def get_mango_config_file():
    return getConfigFile('mango.json')


def getConfigFolder():
    global configPath
    configPath = loadJSON(get_mango_config_file())['config_folder']
    return os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), configPath)


def getConfigFile(file_name):
    global configPath
    return os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), configPath,file_name)


def load_plugin(plugin_name):
    loaded_module = import_module(plugin_name)
    return loaded_module


def execute_module(module_path):
    try:
        loaded_module = load_plugin(module_path)
        instance = loaded_module.instance()
        instance.go()
    except ModuleNotFoundError as e:
        print("Plugin not found : " + str(module_path)+ "("+str(e)+")")


def internet_reachable():
    google_server = 'http://216.58.192.142'
    try:
        urlopen(google_server, timeout=4)
        return True
    except URLError:
        return False
    except RemoteDisconnected:
        return False


