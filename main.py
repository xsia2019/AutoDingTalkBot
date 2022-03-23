from Lib.qWeatherAPI import QWeatherApi
from KEY.qweather_key import qweather_key


qweather_key = qweather_key

if __name__ == '__main__':

    qweather = QWeatherApi(qweather_key)

    # Get the current weather
    city = qweather.get_city_info('Beihai')

    indices = qweather.get_indices('Beihai')
    print(indices)

    my_indice = qweather.get_my_indices('Beihai')
    print(my_indice[0])
    print(my_indice[1])
    print(my_indice[2])
    print(my_indice[3])
    print(my_indice[4])

    pingguo = qweather.get_my_indices('pingguo')
    print(pingguo[0])
    print(pingguo[1])
    print(pingguo[2])
    print(pingguo[3])
    print(pingguo[4])
