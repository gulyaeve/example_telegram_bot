import asyncio
from dataclasses import dataclass

from config import Config
from utils.rest_api import RestAPI


@dataclass
class Weather:
    location_name: str
    description: str
    temp: int
    temp_min: int
    temp_max: int
    wind_speed: int

    def __str__(self):
        msg = f"<b>Погода в {self.location_name}:</b>\n" \
              f"Сейчас <i>{self.description}</i>\n" \
              f"Температура: <i>{self.temp}</i>\n" \
              f"Минимальная температура: <i>{self.temp_min}</i>\n" \
              f"Максимальная температура: <i>{self.temp_max}</i>\n" \
              f"Скорость ветра: <i>{self.wind_speed}м/с</i>\n"
        return msg


class OpenWeatherApi(RestAPI):
    def __init__(self):
        super().__init__(
            rest_link=Config.OpenWeatherConfig.OPENWEATHER_API_LINK,
            rest_token=Config.OpenWeatherConfig.OPENWEATHER_API_TOKEN,
        )
        self._headers = {
            # "Authorization": f"{self._token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def get_weather(self, latitude: float, longitude: float) -> Weather | None:
        params = {
            "appid": f"{self._token}",
            "lat": latitude,
            "lon": longitude,
            "units": "metric",
            "lang": "ru"
        }
        answer = await self.get_json("/data/2.5/weather", params)
        if answer:
            return Weather(
                location_name=answer["name"],
                description=answer["weather"][0]["description"],
                temp=int(answer["main"]["temp"]),
                temp_max=int(answer["main"]["temp_max"]),
                temp_min=int(answer["main"]["temp_min"]),
                wind_speed=int(answer["wind"]["speed"]),
            )
        else:
            return None


# Тестирование API
if __name__ == "__main__":
    api = OpenWeatherApi()
    ans = asyncio.run(api.get_weather(55.814640, 37.404065))
    print(str(ans))
