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
    def parse_command(self, command:str) -> list : 
        if command == "":
            return {'command':"", 'arguments':[]}

        output_command = None
        output_arguments = []

        commands = self.split_with_subcommands(command)
        if len(commands) > 0:
            if commands[0] in self.command_to_instance.keys():
                output_command = commands[0] # Setting command
                if len(commands) > 1:
                    output_arguments = commands[1:] # Setting arguments
        return {'command':output_command, 'arguments':output_arguments}
        
