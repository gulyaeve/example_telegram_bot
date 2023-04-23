import asyncio

from config import Config
from utils.rest_api import RestAPI


class CatApi(RestAPI):
    def __init__(self):
        super().__init__(
            rest_link=Config.CAT_API_LINK,
        )

    async def get_cat_url(self) -> str | None:
        answer = await self.get_json("/v1/images/search", params=None)
        if answer:
            return answer[0]["url"]
        else:
            return None


# Тестирование API
if __name__ == "__main__":
    api = CatApi()
    ans = asyncio.run(api.get_cat_url())
    print(ans)
