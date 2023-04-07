import asyncio
import python_weather

async def get_weather_data(location):
    async with python_weather.Client(format=python_weather.IMPERIAL) as client:
        weather = await client.get(location)
        return weather

def todays_weather(location):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    current_weather = loop.run_until_complete(get_weather_data(location))
    description = current_weather.current.description
    todays_forecast = next(current_weather.forecasts)
    temperature_high = todays_forecast.highest_temperature
    temperature_low = todays_forecast.lowest_temperature
    temperature_avg=todays_forecast.temperature
    precipitation_chance = current_weather.current.precipitation
    return f"{description.capitalize()}. High is {temperature_high} degrees, low is {temperature_low} degrees. Average temperature is {temperature_avg} degrees. Chance of precipitation {precipitation_chance}%."

if __name__ == "__main__":
    print(todays_weather())
