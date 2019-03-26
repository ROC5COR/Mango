import logging

logger = logging.getLogger()

class Scheduler:
    def __init__(self):
        None

    def schedule_plugins(self, plugins_dict:dict):
        plugins = list(set(plugins_dict.values()))
        for plugin in plugins:
            period_data_array = plugin.get_update_period()
            for period_data in period_data_array:
                try:
                    if period_data['time'] is not None:
                        hours = int(period_data['time'][0])
                        minutes = int(period_data['time'][1])
                        logger.info("Must schedule time for "+str(plugin)+" at "+hours+":"+minutes+" "+period_data['period'])
                except Exception as e:
                    logger.error("Can't parse time data for "+str(plugin)+" ("+str(e)+")")
            
            