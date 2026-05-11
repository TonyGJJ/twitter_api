from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

from .config import Settings


class TwtApiError(Exception):
    pass


@dataclass
class TwtApiClient:
    settings: Settings
    timeout: int = 30

    def _headers(self) -> dict[str, str]:
        return {
            "X-API-Key": self.settings.api_key,
            "X-Lang": self.settings.lang,
        }

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.settings.base_url.rstrip('/')}/{path.lstrip('/')}"
        resp = requests.get(url, headers=self._headers(), params=params, timeout=self.timeout)
        resp.raise_for_status()
        payload = resp.json()

        code = payload.get("code")
        if code is not None and code != 200:
            raise TwtApiError(f"TwtAPI 调用失败: code={code}, msg={payload.get('msg')}")

        return payload

    def get_trends(self, woeid: int) -> dict[str, Any]:
        return self._get("/api/v1/twitter/Trends", params={"woeid": woeid})

    def search_tweets(
        self,
        q: str,
        result_type: str = "Top",
        count: int = 20,
    ) -> dict[str, Any]:
        return self._get(
            "/api/v1/twitter/Search",
            params={"q": q, "type": result_type, "count": count},
        )

    def get_user_by_screen_name(self, username: str) -> dict[str, Any]:
        return self._get(
            "/api/v1/twitter/UserResultByScreenName",
            params={"username": username},
        )

    def get_tweet_detail(self, tweet_id: str) -> dict[str, Any]:
        return self._get("/api/v1/twitter/TweetDetail", params={"tweet_id": tweet_id})
