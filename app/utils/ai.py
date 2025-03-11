import asyncio
import os

import httpx
from fastapi_mongo_base.utils import basic

promptly_semaphore = asyncio.Semaphore(8)


class PromptlyClient(httpx.AsyncClient):

    def __init__(self):
        super().__init__(
            base_url=os.getenv("PROMPTLY_URL"),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "x-api-key": os.getenv("UFILES_API_KEY"),
            },
        )

    @basic.try_except_wrapper
    @basic.retry_execution(attempts=3, delay=1)
    async def ai_image(
        self, image_url: str, key: str, data: dict = {}, **kwargs
    ) -> dict:
        async with promptly_semaphore:
            timeout = kwargs.pop("timeout", 30)
            r = await self.post(
                f"/image/{key}",
                json={**data, "image_url": image_url},
                timeout=timeout,
                **kwargs,
            )
            r.raise_for_status()
            return r.json()

    @basic.try_except_wrapper
    @basic.retry_execution(attempts=3, delay=1)
    async def ai(self, key: str, data: dict = {}, **kwargs) -> dict:
        async with promptly_semaphore:
            timeout = kwargs.pop("timeout", 30)
            r = await self.post(f"/{key}", json=data, timeout=timeout, **kwargs)
            r.raise_for_status()
            return r.json()

    async def ai_search(self, key: str, data: dict = {}, **kwargs) -> dict:
        async with promptly_semaphore:
            timeout = kwargs.pop("timeout", 30)
            return await self.post(f"/search/{key}", data, timeout=timeout, **kwargs)

    async def translate(self, text: str, language: str = "Persian", **kwargs) -> str:
        timeout = kwargs.pop("timeout", 30)
        resp: dict = await self.ai(
            "translate",
            dict(text=text, target_language=language),
            timeout=timeout,
            **kwargs,
        )

        return resp.get("translated_text")
