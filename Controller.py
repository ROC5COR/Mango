import PluginLoader
import Scheduler
import Interpreter
import CommandLineInteface
import ParameterManager
import logging


logger = logging.getLogger()

pm = ParameterManager.ParamameterManager('main','config.json')

class Controller:
    def __init__(self):
        identity = pm.get_param('identity',"SAP") # SimpleAssistantProgram
        version = pm.get_param('version', "0.0.0")

        pl = PluginLoader.PluginLoader()

        plugin_paths = pm.get_param('plugin_paths',["plugins"])
        for plugin_path in plugin_paths:
            pl.load_plugins(plugin_path)

        plugins = pl.get_plugins()
        
        schl = Scheduler.Scheduler()
        schl.schedule_plugins(plugins)

        inter = Interpreter.Interpreter()
        inter.set_plugins(plugins)
        
        user_interface = CommandLineInteface.CommandLineInterface()
        while True:
            user_input = user_interface.wait_for_input()
            if user_input == 'exit':
                break
            
            user_commands = inter.parse_command(user_input)
            if user_commands['command'] is not None and user_commands['command'] != "":
                plugins[user_commands['command']].go(user_commands['arguments'], message_listener=user_interface)
            elif user_commands['command'] == "":
                None
            else:
                logger.error('Command: unknown')