import utils
from distutils.version import StrictVersion
from importlib import import_module

# Variables
mango_version = StrictVersion('0.0.0')  # default value
config_path = "default_config"  # default value
plugins_path = "plugins"

# Functions
def init():
    print("[Init]")
    global config_path
    config_path = get_config_folder()

    global mango_version
    mango_version = utils.loadJSON(get_mango_config_file())['mango_version']

    global plugins_path
    plugins_path = utils.getPluginsPath()

    print("[Init] : OK")
    return 1


def get_config_folder():
    return utils.loadJSON(get_mango_config_file())['config_folder']

def get_plugins_folder():
    return utils.loadJSON(get_mango_config_file())['plugins_path']

def show_all_plugin():
    plugin_names = utils.loadJSON(get_mango_config_file())['all_plugins']
    for plugin_name in plugin_names:
        execute_module('plugins.' + plugin_name)


def show_normal_plugin():
    plugin_names = utils.loadJSON(get_mango_config_file())['normal_plugins']
    for plugin_name in plugin_names:
        execute_module('plugins.' + plugin_name)


def get_mango_config_file():
    return utils.getMangoFile()


def load_plugin(plugin_name):
    loaded_module = import_module(plugin_name)
    return loaded_module


def execute_module(module_path: str, args=[]):
    try:
        loaded_module = load_plugin(module_path)
        instance = loaded_module.instance()
        instance.go(args)
    except ModuleNotFoundError as e:
        print("Plugin not found : " + str(module_path) + "(" + str(e) + ")")


def parse_command(command: list):
    if command[0] == "":
        return 1
    elif command[0] == "exit":
        print("Bye")
        return 0
    else:
        return execute_module('plugins.' + str(command[0]), command[1:])
