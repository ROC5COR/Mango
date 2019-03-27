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
        self.identity = pm.get_param('identity',"SAP") # SimpleAssistantProgram
        self.version = pm.get_param('version', "0.0.1")
        pm.set_param("user_identity","User")

        logger.info("Starting... "+self.identity+" "+self.version)

        self.plugin_loader = PluginLoader.PluginLoader()

        plugin_paths = pm.get_param('plugin_paths',["plugins"])
        for plugin_path in plugin_paths:
            self.plugin_loader.load_plugins(plugin_path)

        self.plugins = self.plugin_loader.get_plugins()
        
        self.scheduler = Scheduler.Scheduler()
        self.scheduler.schedule_plugins(self.plugins)

        self.interpreter = Interpreter.Interpreter()
        self.interpreter.set_plugins(self.plugins)

        self.user_interface = None # No User interface defined ar this point
        
    def start_cli(self):
        self.user_interface = CommandLineInteface.CommandLineInterface()
        while True:
            user_input = self.user_interface.wait_for_input()
            user_commands = self.interpreter.parse_command(user_input)
            if user_commands['commands'] is not None and len(user_commands['commands']) > 0:
                command = user_commands['commands'][0]
                if user_commands['is_plugin'] == True:
                    self.plugins[command].go(user_commands['commands'][1:], message_listener=self.user_interface)
                elif command == "exit":
                    break
                else:
                    logger.error('Command: unknown')


if __name__ == "__main__":
    ctrl = Controller()
    ctrl.start_cli()