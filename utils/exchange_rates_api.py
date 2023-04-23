import asyncio

from config import Config
from utils.rest_api import RestAPI


class ExchangeRatesApi(RestAPI):
    def __init__(self):
        super().__init__(
            rest_link=Config.ExchangeRatesConfig.EXCHANGE_RATES_API_LINK,
            rest_token=Config.ExchangeRatesConfig.EXCHANGE_RATES_API_TOKEN,
        )
        self._headers = {
            "apikey": f"{self._token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def get_exchange(self, exchange_from: str, exchange_to: str, amount: int) -> int | None:
        params = {
            "from": exchange_from,
            "to": exchange_to,
            "amount": amount
        }
        answer = await self.get_json("/exchangerates_data/convert", params)
        if answer:
            return int(answer["result"])
        else:
            return None


# Тестирование API
if __name__ == "__main__":
    api = ExchangeRatesApi()
    ans = asyncio.run(api.get_exchange("USD", "RUB", 100))
    print(ans)
