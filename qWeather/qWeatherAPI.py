#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import json
from bs4 import BeautifulSoup
from KEY.qweather_key import qweather_key

''' official website  https://www.qweather.com '''
'''      dev website  https://dev.qweather.com'''

qweather_key = qweather_key


class QWeatherApi:
    def __init__(self, key=qweather_key):
        # 自定义headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.132 Safari/537.36'}
        self.key = qweather_key

        # 城市信息查询API链接
        self.url_api_geo = 'https://geoapi.qweather.com/v2/city/lookup?'
        # 实时天气API链接
        self.url_api_weather_now = 'https://devapi.qweather.com/v7/weather/now'

        # 天气预报API链接城市天气API链接
        self.url_api_weather = 'https://devapi.qweather.com/v7/weather/'

        self.url_api_geo = 'https://geoapi.qweather.com/v2/city/'
        self.url_api_rain = 'https://devapi.qweather.com/v7/minutely/5m'

        self.url_api_air = 'https://devapi.qweather.com/v7/air/now'
        # 生活指数API链接
        self.url_api_indices = 'https://devapi.qweather.com/v7/indices/1d?'
        # 灾害报警API链接
        'https://devapi.qweather.com/v7/warning/now?'
        # 灾害预警API链接
        'https://devapi.qweather.com/v7/warning/list?'

    def get_city_info(self, city_kw):
        url = self.url_api_geo + 'lookup?location=' + city_kw + '&key=' + self.key
        city = requests.get(url, headers=self.headers, timeout=30).json()['location'][0]

        city_id = city['id']
        district_name = city['name']
        city_name = city['adm2']
        province_name = city['adm1']
        country_name = city['country']
        lat = city['lat']
        lon = city['lon']
        # 返回 城市ID，城市区名，城市名，省份名，国家名，纬度，经度，
        return city_id, district_name, city_name, province_name, country_name, lat, lon

    def get_weather_now(self, city_id):
        url = '{url}?location={id}&key={key}'.format(url=self.url_api_weather_now, id=city_id, key=self.key)
        result = requests.get(url, headers=self.headers, timeout=30).json()

        fxLink = result['fxLink']  # 风向链接
        weather_info = result['now']

        text = weather_info['text']                 # 白天天气
        temp = weather_info['temp']                 # 实时温度
        feelsLike = weather_info['feelsLike']       # 体感温度
        windDir = weather_info['windDir']           # 风速
        windScale = weather_info['windScale']       # 风向
        humidity = weather_info['humidity']         # 湿度

        return text, temp, feelsLike, windDir, windScale, humidity, fxLink

    def get_weather_forecast(self):
        fxLink = 'https://www.qweather.com/weather/beihai-101301301.html'
        result = requests.get(fxLink, headers=self.headers, timeout=30).text
        # soup = BeautifulSoup(result, 'lxml')
        soup = BeautifulSoup(result, 'html.parser')
        weather = soup.find('div', class_='current-abstract').text.strip()
        return weather



#
# def get(api_type):
#     url = url_api_weather + api_type + '?location=' + city_id + mykey
#     return requests.get(url).json()
#
#
# def rain(lat, lon):
#     url = url_api_rain + '?location=' + lat + ',' + lon + mykey
#     return requests.get(url).json()
#
#
# def air(city_id):
#     url = url_api_air + '?location=' + city_id + mykey
#     return requests.get(url).json()
#
#
# def now():
#     return get_now['now']
#
#
# def daily():
#     return get_daily['daily']
#
#
# def hourly():
#     return get_hourly['hourly']
#
#
# if __name__ == '__main__':
#     if KEY == '':
#         print('No Key! Get it first!')
#
#     print('请输入城市:')
#     city_input = input()
#     city_idname = get_city(city_input)
#
#     city_id = city_idname[0]
#
#     get_now = get('now')
#     get_daily = get('3d')  # 3d/7d/10d/15d
#     get_hourly = get('24h')  # 24h/72h/168h
#     get_rain = rain(city_idname[5], city_idname[6])  # input longitude & latitude
#     air_now = air(city_id)['now']
#
#     # print(json.dumps(get_now, sort_keys=True, indent=4))
#     if city_idname[2] == city_idname[1]:
#         print(city_idname[3], str(city_idname[2]) + '市')
#     else:
#         print(city_idname[3], str(city_idname[2]) + '市', str(city_idname[1]) + '区')
#     print('当前天气：', get_now['now']['text'], get_now['now']['temp'], '°C', '体感温度', get_now['now']['feelsLike'], '°C')
#     print('空气质量指数：', air_now['aqi'])
#     print('降水情况：', get_rain)
#     print('今日天气：', daily()[0]['textDay'], daily()[0]['tempMin'], '-', daily()[0]['tempMax'], '°C')
#
#     nHoursLater = 1  # future weather hourly
#     print(nHoursLater, '小时后天气：', hourly()[1]['text'], hourly()[1]['temp'], '°C')
#
#     nDaysLater = 1  # future weather daily
#     print(nDaysLater, '天后天气：', daily()[nDaysLater]['textDay'], daily()[nDaysLater]['tempMin'], '-',
#           daily()[nDaysLater]['tempMax'], '°C')
