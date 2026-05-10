from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str = "https://api.twtapi.com"
    lang: str = "zh"


def load_settings() -> Settings:
    load_dotenv()

    api_key = os.getenv("TWTAPI_API_KEY", "").strip()
    base_url = os.getenv("TWTAPI_BASE_URL", "https://api.twtapi.com").strip()
    lang = os.getenv("TWTAPI_LANG", "zh").strip()

    if not api_key:
        raise ValueError("缺少 TWTAPI_API_KEY。请先配置 .env 文件。")

    return Settings(api_key=api_key, base_url=base_url, lang=lang)
