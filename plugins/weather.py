import datetime
import json
import time
from urllib.request import urlopen

import pyowm
from prettytable import PrettyTable

import utils

def instance():
    return Weather()

class Weather(object):
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

    def go(self, args):
        if not utils.internet_reachable():
            print("Weather : Offline")
            return -1

        #obs = self.owm.weather_at_coords(self.currentLocation['latitude'],self.currentLocation['longitude'])
        print('[WTHR/FRCST]')
        fcast = self.owm.three_hours_forecast(self.cities[0])
        if time.localtime().tm_hour < 8:
            print('In ' + fcast.get_forecast().get_location().get_name() + ' there will be ' + fcast.get_weather_at(
                self.morningTime).get_detailed_status() + ' this morning')
        elif time.localtime().tm_hour >= 8 and time.localtime().tm_hour < 20:
            print('In '+fcast.get_forecast().get_location().get_name()+' there will be '+fcast.get_weather_at(
                self.eveningTime).get_detailed_status()+' this evening')
        else:
            print('In ' + fcast.get_forecast().get_location().get_name() + ' there will be ' + fcast.get_weather_at(
                self.tomorrowTime).get_detailed_status() + ' tomorrow')

        print("")

        for city in self.cities:
            obs = self.owm.weather_at_place(city)
            city = obs.get_location().get_name()+', '+obs.get_location().get_country()
            conditions = obs.get_weather().get_detailed_status()
            temperature = round(obs.get_weather().get_temperature()['temp'] - 273.15,1)
            wind = obs.get_weather().get_wind()['speed']
            humidity = obs.get_weather().get_humidity()
            self.table.add_row([city,conditions,temperature,wind,humidity])
        print('[WTHR]')
        print(self.table)