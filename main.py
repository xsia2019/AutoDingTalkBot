from Lib.qWeatherAPI import QWeatherApi
from KEY.qweather_key import qweather_key

if __name__ == '__main__':

    weather = QWeatherApi(key=qweather_key)
    city_beihai = weather.get_city_info('北海')
    city_beijing = weather.get_city_info('北京')
    beihai_now = weather.get_weather_now(city_beihai[0])
    beijing_now = weather.get_weather_now(city_beijing[0])

    forcast_beihai = weather.get_weather_forecast()

    print(city_beihai, city_beijing)
    print(beihai_now, beijing_now)

    print(forcast_beihai)