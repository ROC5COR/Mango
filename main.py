import sys
import utils

# Functions
def get_config_folder():
    return utils.loadJSON(utils.get_mango_config_file())['config_folder']


def show_all_plugin():
    plugin_names = utils.loadJSON(utils.get_mango_config_file())['all_plugins']
    for plugin_name in plugin_names:
        utils.execute_module('plugins.'+plugin_name)


def show_normal_plugin():
    plugin_names = utils.loadJSON(utils.get_mango_config_file())['normal_plugins']
    for plugin_name in plugin_names:
        utils.execute_module('plugins.'+plugin_name)


def parse_command(command):
    if command[0] == "":
        return 1
    elif command[0] == "exit":
        return 0
    elif command[0] == "finance":
        utils.execute_module('plugins.finance')
    elif command[0] == "fdj" or sys.argv[1] == "fete":
        utils.execute_module('plugins.fetedujour')
    elif command[0] == "weather":
        utils.execute_module('plugins.weather')
    elif command[0] == "uart":
        utils.execute_module('plugins.uart')
    elif command[0] == "moon":
        utils.execute_module('plugins.moon')
    elif command[0] == "calc":
        utils.execute_module('plugins.calc')
    else:
        print("Module not found")
        return -1
    return 1

#######MAIN#######
print("Cutting the mango")


if len(sys.argv) > 1: # An arguments was passed
    if sys.argv[1] == ('--all' or '-a' or 'all'):
        show_all_plugin()
        print("Mango in plate")
    elif sys.argv[1] == ('-i' or '--interactive'):
        while(True):
            try:
                user_input = str(input("MANGO> "))
                user_inputs = user_input.split(' ') # TODO change to manage '"' that make sub-strings
                result = parse_command(user_inputs)
                if result == 0:
                    break;
            except KeyboardInterrupt:
                print("Exiting")
                break;
    else:
        if parse_command(sys.argv[1:]) < 0:
            print("Rotten mango !")
        else:
            print("Mango in plate")

else:
    show_normal_plugin()
    print("Mango in plate")




