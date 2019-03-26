import datetime
import time
import pyowm
from prettytable import PrettyTable
import utils
from Plugin import Plugin
from MessageListener import MessageListener


def instance():
    return Weather()

class Weather(Plugin):
    def __init__(self):
        self.cities = []
        cities = utils.loadJSON(utils.getConfigFile('weather.json'))['cities']
        for city in cities:
            self.cities.append(city)
        api_key = utils.loadJSON(utils.getConfigFile('weather.json'))['api_key']

        self.table = PrettyTable(['City', 'Conditions', 'Temp [°C]', 'Wind', 'Humidity'])
        self.owm = pyowm.OWM(api_key)
        self.owm.set_language('en')
        self.eveningTime = datetime.datetime.now().replace(hour=20, minute=0)
        self.morningTime = datetime.datetime.now().replace(hour=8, minute=0)
        self.tomorrowTime = (datetime.datetime.now().replace(hour=16, minute=0)+datetime.timedelta(days=1))

    def go(self, args:list, message_listener:MessageListener = MessageListener()):
        if not utils.internet_reachable():
            print("[Weather] : Can't reach the internet")
            return -1

        if len(args) == 0:
            #obs = self.owm.weather_at_coords(self.currentLocation['latitude'],self.currentLocation['longitude'])
            message_listener.printMessage('[WTHR/FRCST]')
            fcast = self.owm.three_hours_forecast(self.cities[0])
            if time.localtime().tm_hour < 8:
                message_listener.printMessage('In ' + fcast.get_forecast().get_location().get_name() + ' there will be ' + fcast.get_weather_at(
                    self.morningTime).get_detailed_status() + ' this morning')
            elif time.localtime().tm_hour >= 8 and time.localtime().tm_hour < 20:
                city_name = fcast.get_forecast().get_location().get_name()
                detailled_status = fcast.get_weather_at(self.eveningTime).get_detailed_status()
                message_listener.printMessage('In '+city_name+' there will be '+detailled_status+' this evening')
            else:
                message_listener.printMessage('In ' + fcast.get_forecast().get_location().get_name() + ' there will be ' + fcast.get_weather_at(
                    self.tomorrowTime).get_detailed_status() + ' tomorrow')

            message_listener.printMessage("\n")

            self.table.clear_rows()
            for city in self.cities:
                obs = self.owm.weather_at_place(city)
                city = obs.get_location().get_name()+', '+obs.get_location().get_country()
                conditions = obs.get_weather().get_detailed_status()
                temperature = round(obs.get_weather().get_temperature()['temp'] - 273.15,1)
                wind = obs.get_weather().get_wind()['speed']
                humidity = obs.get_weather().get_humidity()
                self.table.add_row([city,conditions,temperature,wind,humidity])
            message_listener.printMessage('[WTHR]')
            message_listener.printMessage(self.table.get_string())

        elif len(args) == 1: # Assuming that we have a city in parameter
            message_listener.printMessage('[WTHR/FRCST]')
            fcast = self.owm.three_hours_forecast(args[0])
            if time.localtime().tm_hour < 8:
                message_listener.printMessage(
                    'In ' + fcast.get_forecast().get_location().get_name() + ' there will be ' + fcast.get_weather_at(
                        self.morningTime).get_detailed_status() + ' this morning')
            elif time.localtime().tm_hour >= 8 and time.localtime().tm_hour < 20:
                message_listener.printMessage(
                    'In ' + fcast.get_forecast().get_location().get_name() + ' there will be ' + fcast.get_weather_at(
                        self.eveningTime).get_detailed_status() + ' this evening')
            else:
                message_listener.printMessage(
                    'In ' + fcast.get_forecast().get_location().get_name() + ' there will be ' + fcast.get_weather_at(
                        self.tomorrowTime).get_detailed_status() + ' tomorrow')

            message_listener.printMessage("\n")

            obs = self.owm.weather_at_place(args[0])
            city = obs.get_location().get_name() + ', ' + obs.get_location().get_country()
            conditions = obs.get_weather().get_detailed_status()
            temperature = round(obs.get_weather().get_temperature()['temp'] - 273.15, 1)
            wind = obs.get_weather().get_wind()['speed']
            humidity = obs.get_weather().get_humidity()
            self.table.add_row([city, conditions, temperature, wind, humidity])
            message_listener.printMessage('[WTHR]')
            message_listener.printMessage(self.table.get_string())