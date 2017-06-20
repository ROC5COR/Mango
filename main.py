import sys
from builtins import ModuleNotFoundError

import utils
from plugins.fetedujour import fetedujour
from plugins.finance import finance
from plugins.greetings import greetings
from plugins.weather import weather

### Variables
plugin_instances = {}
config_folder = "/config_perso" #default value

###Functions
def get_config_folder():
	return utils.loadJSON(utils.getMangoPath() +'/mango.json')['config_folder']

def show_all_plugin():
	plugin_names = utils.loadJSON(utils.getMangoPath() +'/mango.json')['all_plugins']
	for plugin_name in plugin_names:
		try:
			loaded_module = utils.load_plugin('plugins.'+plugin_name)
			plugin_instances[plugin_name] = loaded_module.instance()
			plugin_instances[plugin_name].go()
		except ModuleNotFoundError:
			print("Plugin not found : "+str(plugin_name))

def show_normal_plugin():
	plugin_names = utils.loadJSON(utils.getMangoPath() +'/mango.json')['normal_plugins']
	for plugin_name in plugin_names:
		try:
			loaded_module = utils.load_plugin('plugins.' + plugin_name)
			plugin_instances[plugin_name] = loaded_module.instance()
			plugin_instances[plugin_name].go()
		except ModuleNotFoundError:
			print("Plugin not found : " + str(plugin_name))


#######MAIN#######
print("Cutting the mango")
print(config_folder)
if len(sys.argv) > 1: #An arguments was passed
	if sys.argv[1] == "all":
		show_all_plugin()
	elif sys.argv[1] == "finance":
		market = finance()
		market.go()
	elif sys.argv[1] == "fdj" or sys.argv[1] == "fete":
		fete = fetedujour()
		fete.go()
	elif sys.argv[1] == "weather":
		weather =weather()
		weather.go()
	else:
		print("Rotten mango")
else:
	show_normal_plugin()

print("Mango in plate")

