import os
from importlib import import_module
from MessageListener import MessageListener


import Plugin
import utils
import ClientConnection

# Static functions for simplicity
def get_parameter(parameter_name: str):
    return utils.loadJSON(Mango.get_mango_config_file())[parameter_name]


def get_config_folder():
    return utils.loadJSON(Mango.get_mango_config_file())['config_folder']


def get_plugins_folder():
    return utils.loadJSON(Mango.get_mango_config_file())['plugins_path']


def get_plugins_path():
    return utils.getAbsoluteFilePath(get_plugins_folder())


class Mango():
    def __init__(self):
        print("[Init]")

        self.config_path = get_config_folder()  # default value
        self.plugins_path = get_plugins_path()
        self.command_to_plugin_path = dict() # Store command name to plugin path
        self.module_path_to_plugin_instance = dict() # Store plugin path => instance
        self.is_server_running = False
        self.server_file = "server_started"
        self.config_path = get_config_folder()
        self.version = utils.loadJSON(Mango.get_mango_config_file())['version']
        self.plugins_path = utils.getPluginsPath()

        self.load_modules()

        print("[Init] : OK")

    def load_modules(self):
        objects = os.listdir(self.plugins_path)

        for i in objects:
            if i.endswith('.py'):
                try:
                    plugin_path = get_plugins_folder() + '.' + i[0:-3]
                    loaded_module = self.load_plugin(plugin_path)  # Instanciate
                    instance = loaded_module.instance()
                    self.command_to_plugin_path[i[0:-3]] = plugin_path
                    self.module_path_to_plugin_instance[plugin_path] = instance

                    if not issubclass(instance.__class__, Plugin.Plugin):
                        print("[MANGO] Warning : This is not a subclass of mango_plugin")
                    else:
                        aliases = instance.get_aliases()
                        for alias in aliases:
                            self.command_to_plugin_path[alias] = plugin_path

                except ModuleNotFoundError as e:
                    print("Plugin not found : " + str(plugin_path) + "(" + str(e) + ")")
                except e:
                    print("Error as occurred while loading module (" + str(e) + ")")

        for k in self.command_to_plugin_path:
            print(k, "=>", self.command_to_plugin_path[k])

        print("[MANGO] All modules loaded")

    """def show_normal_plugin(self):
        plugin_names = utils.loadJSON(Mango.get_mango_config_file())['normal_plugins']
        for plugin_name in plugin_names:
            self.execute_module('plugins.' + plugin_name)

    def show_all_plugin(self):
        plugin_names = utils.loadJSON(Mango.get_mango_config_file())['all_plugins']
        for plugin_name in plugin_names:
            self.execute_module('plugins.' + plugin_name)"""

    def parse_message_with_server(self, message: str):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = int(get_parameter('mango_server_port'))
        s.connect(("", port))

        s.send(message.encode('utf-8'))
        r = s.recv(4096)
        print(r.decode('utf-8'))

    def start_server(self):
        import socket
        import os

        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = int(get_parameter('mango_server_port'))
        print("[MANGO] Starting server on port: ", port)
        # socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket.bind(('', port))
        self.is_server_running = True
        with open(self.server_file, "w") as f:
            f.write("ok")
            f.close()

        try:
            while True:
                socket.listen(5)
                (clientsocket, (ip, port)) = socket.accept()
                newClient = ClientConnection.ClientConnection(ip, port, clientsocket, self)
                newClient.start()
        except KeyboardInterrupt:
            print("Server stopped")

        os.remove(self.server_file)
        print("Server ended")
        socket.close()

    def load_plugin(self, plugin_name):
        return import_module(plugin_name)

    def execute_module(self, module_path: str, args=[]):
        try:
            loaded_module = self.load_plugin(module_path)
            instance = loaded_module.instance()

            if not issubclass(instance.__class__, Plugin.Plugin):
                print("[MANGO] Warning : This is not a subclass of mango_plugin")
            print(instance.get_aliases())

            instance.go(args)
        except ModuleNotFoundError as e:
            print("Plugin not found : " + str(module_path) + "(" + str(e) + ")")
        except:
            print("Error while executing plugin: "+str(module_path)+" ("+str(e)+")")

    def parse_command(self, command: list, message_listener: MessageListener = MessageListener()):
        """

        :param command: List of string commands
        :return: 1 if ok, 0 if quit, -1 if error
        """
        if command[0] == "":
            return 1
        elif command[0] == "exit":
            message_listener.printMessage("Bye")
            return 0
        else:
            if command[0] in self.command_to_plugin_path:
                if self.command_to_plugin_path[command[0]] in self.module_path_to_plugin_instance:
                    inst = self.module_path_to_plugin_instance[self.command_to_plugin_path[command[0]]]
                    inst.go(command[1:], message_listener=message_listener)
                    return 1
                else:
                    message_listener.printMessage("Error : No instance of the module found")
                    return -1
            else:
                message_listener.printMessage("Error : No module named : " + command[0])
                return -1

    def is_server_online(self):
        import os
        if os.path.exists(self.server_file):
            return True
        else:
            return False

    def get_version(self):
        return self.version

    @staticmethod
    def get_mango_config_file():
        return utils.getAbsoluteFilePath('mango.json')

