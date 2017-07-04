import sys
import argparse

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


#######MAIN#######
print("Cutting the mango")
#print('Config folder : '+utils.getConfigFolder())
if len(sys.argv) > 1: # An arguments was passed
    if sys.argv[1] == "all":
        show_all_plugin()
    elif sys.argv[1] == "finance":
        utils.execute_module('plugins.finance')
    elif sys.argv[1] == "fdj" or sys.argv[1] == "fete":
        utils.execute_module('plugins.fetedujour')

    elif sys.argv[1] == "weather":
        utils.execute_module('plugins.weather')
    elif sys.argv[1] == "uart":
        utils.execute_module('plugins.uart')
    else:
        print("Rotten mango")
else:
    show_normal_plugin()

print("Mango in plate")

