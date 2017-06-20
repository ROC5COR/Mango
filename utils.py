import sys
import json
import os
import inspect
from importlib.util import spec_from_file_location, module_from_spec
from importlib import import_module

def loadJSON(file_name):
	file = open(file_name)
	data = json.loads(file.read())
	return data

def getMangoPath():
	return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def load_plugin(plugin_name):
    loaded_module = import_module(plugin_name)
    return loaded_module


