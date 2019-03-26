import logging
import os
from importlib import import_module

import Plugin

logger = logging.getLogger()

class PluginLoader:
    def __init__(self):
        self.plugin_to_instance = dict()
    
    def load_plugins(self, folder: str):
        for i in os.listdir(folder):
            if i.endswith('.py'):
                try:
                    plugin_path = folder + '.' + i[0:-3]
                    loaded_module = import_module(plugin_path)  # Loading Python module
                    instance = loaded_module.instance() # Instantiate 

                    self.plugin_to_instance[i[0:-3]] = instance

                    if not issubclass(instance.__class__, Plugin.Plugin):
                        logger.warning("Warning : This is not a subclass of mango_plugin")
                    else:
                        aliases = instance.get_aliases()
                        for alias in aliases:
                            #self.command_to_plugin_path[alias] = plugin_path
                            self.plugin_to_instance[alias] = instance

                except ModuleNotFoundError as e:
                    logger.error("Plugin not found : " + str(plugin_path) + "(" + str(e) + ")")
                except Exception as e:
                    logger.error("Error as occurred while loading module "+plugin_path+" (" + str(e) + ")")

        for k in self.plugin_to_instance:
            print(k, "=>", self.plugin_to_instance[k])

        logger.info("PluginLoader: All modules loaded")
        

    def get_plugins(self):
        return self.plugin_to_instance




