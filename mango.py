import os
from distutils.version import StrictVersion
from importlib import import_module
from MessageListener import MessageListener

from sqlalchemy.ext.indexable import index_property

import mango_plugin
import utils
import ClientConnection

# Variables
mango_version = StrictVersion('0.0.0')  # default value
config_path = "home_config"  # default value
plugins_path = "plugins"
command_to_module_path = dict()
module_path_to_module_instance = dict()
is_server_running = False

# Functions
def init():
    print("[Init]")
    global config_path
    config_path = get_config_folder()

    global mango_version
    mango_version = utils.loadJSON(get_mango_config_file())['mango_version']

    global plugins_path
    plugins_path = utils.getPluginsPath()

    load_modules()

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

        if not issubclass(instance.__class__, mango_plugin.mango_plugin):
            print("[MANGO] Warning : This is not a subclass of mango_plugin")
        print(instance.get_aliases())

        instance.go(args)
    except ModuleNotFoundError as e:
        print("Plugin not found : " + str(module_path) + "(" + str(e) + ")")



def load_modules():
    global command_to_module_path
    global plugins_path
    global module_path_to_module_instance

    objects = os.listdir(plugins_path)

    for i in objects:
        if i.endswith('.py'):

            try:
                plugin_path = get_plugins_folder() + '.' + i[0:-3]
                loaded_module = load_plugin(plugin_path) # Instanciate
                instance = loaded_module.instance()
                command_to_module_path[i[0:-3]] = plugin_path # Store command => plugin path
                module_path_to_module_instance[plugin_path] = instance # Store plugin path => instance

                if not issubclass(instance.__class__, mango_plugin.mango_plugin):
                    print("[MANGO] Warning : This is not a subclass of mango_plugin")
                else:
                    aliases = instance.get_aliases()
                    for alias in aliases:
                        command_to_module_path[alias] = plugin_path

            except ModuleNotFoundError as e:
                print("Plugin not found : " + str(plugin_path) + "(" + str(e) + ")")
            except Exception as e:
                print("Error as occured while loading module ("+str(e)+")")

    for k in command_to_module_path:
        print(k,"=>",command_to_module_path[k])

    print("[MANGO] All modules loaded")


def parse_command(command: list, message_listener:MessageListener = MessageListener() ):
    """

    :param command: List of string commands
    :return: state
    """
    if command[0] == "":
        return 1
    elif command[0] == "exit":
        message_listener.printMessage("Bye")
        return 0
    else:
        if command[0] in command_to_module_path:
            if command_to_module_path[command[0]] in module_path_to_module_instance:
                inst = module_path_to_module_instance[command_to_module_path[command[0]]]
                inst.go(command[1:], message_listener=message_listener)
                return 1
            else:
                message_listener.printMessage("Error : No instance of the module found")
                return -1
        else:
            message_listener.printMessage("Error : No module named : "+command[0])
            return -1

def get_parameter(parameter_name: str):
    return utils.loadJSON(get_mango_config_file())[parameter_name]


def start_server():
    global is_server_running
    import socket
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(get_parameter('mango_server_port'))
    print("[MANGO] Starting server on port: ",port)
    #socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket.bind(('', port))
    is_server_running = True
    while True:
        socket.listen(5)
        (clientsocket, (ip, port)) = socket.accept()
        newClient = ClientConnection.ClientConnection(ip, port, clientsocket)
        newClient.start()


    print("Server ended")
    socket.close()