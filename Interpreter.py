import shlex

class Interpreter:
    def __init__(self):
        self.command_to_instance = dict()

    def set_plugins(self, plugin_dict:dict):
        self.command_to_instance = plugin_dict


    def split_with_subcommands(self, command:str) -> list : 
        return shlex.split(command)

    """
        Receive textual input and transform it to valid array of command + arguments
    """
    def parse_command(self, command_str:str) -> list : 
        if command_str == "":
            return {'commands':"", 'arguments':[]}

        commands = self.split_with_subcommands(command_str)
        is_plugin = False
        if len(commands) > 0:
            if commands[0] in self.command_to_instance.keys():
                is_plugin = True
            else:
                is_plugin = False
                
        return {'commands':commands, 'is_plugin':is_plugin}
        
