import requests
import json
import random
import os

from prefect import task, flow
from pyspark.sql import SparkSession
from dotenv import load_dotenv
from typing import List
from pyspark.sql import DataFrame

load_dotenv()

api_key = os.getenv('WEATHER_API_KEY')
base_url = 'http://api.openweathermap.org/data/2.5/weather'

spark = SparkSession.builder.appName('Weather').getOrCreate()

city_options = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
cities = random.sample(city_options, 3)

@task
def get_weather(cities: List[str]) -> DataFrame:
    weather_data = None

    for city in cities:
        params = {
            'q': city,
            'appid': api_key,
            'units': 'imperial'
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        temperature = data['main']['temp']
        wind_speed = data['wind']['speed']
        humidity = data['main']['humidity']

        new_weather_data = spark.createDataFrame([(city, temperature, wind_speed, humidity)], 
                                             ['city', 'temperature', 'wind_speed', 'humidity'])
        if weather_data is None:
            weather_data = new_weather_data
        else:
            weather_data = weather_data.union(new_weather_data)
    
    return weather_data


@task
def process_data(weather_data: DataFrame) -> DataFrame:
    processed_weather_data = weather_data.filter('temperature > 32') \
        .groupBy('city') \
        .agg({'temperature': 'avg', 'wind_speed': 'avg', 'humidity': 'avg'}) \
        .withColumnRenamed('avg(temperature)', 'avg_temperature') \
        .withColumnRenamed('avg(wind_speed)', 'avg_wind_speed') \
        .withColumnRenamed('avg(humidity)', 'avg_humidity')

    return processed_weather_data


@task 
def write_out_results(weather_data: DataFrame):
    weather_data.show()


@flow
def prefect_run():
    weather = get_weather(cities)
    processed_weather = process_data(weather)
    write_out_results(processed_weather)


if __name__ == '__main__':
    prefect_run()