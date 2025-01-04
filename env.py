from pprint import pprint
from typing import Literal, Union
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()


class Env(BaseModel):
    ENV: Literal["development", "production"] = Field(default="development")
    TELEGRAM_BOT_TOKEN: str
    MINI_APP_DEEPLINK: str
    API_BASE_URL: str
    API_KEY: str


_ENV = os.environ.get("ENV", "development")
_TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
_MINI_APP_DEEPLINK = os.environ.get("MINI_APP_DEEPLINK")
_API_BASE_URL = os.environ.get("API_BASE_URL")
_API_KEY = os.environ.get("API_KEY")

if not _TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "Environment variables not complete: TELEGRAM_BOT_TOKEN is required"
    )

if not _API_BASE_URL:
    raise ValueError("Environment variables not complete: API_BASE_URL is required")

if not _MINI_APP_DEEPLINK:
    raise ValueError(
        "Environment variables not complete: MINI_APP_DEEPLINK is required"
    )

if not _API_KEY:
    raise ValueError("Environment variables not complete: API_KEY is required")


env = Env(
    ENV=_ENV,  # type: ignore
    TELEGRAM_BOT_TOKEN=_TELEGRAM_BOT_TOKEN,
    MINI_APP_DEEPLINK=_MINI_APP_DEEPLINK,
    API_BASE_URL=_API_BASE_URL,
    API_KEY=_API_KEY,
)

print("[env.py] Environment variables loaded successfully")
print("==============================================")
pprint(env.model_dump())
print("==============================================\n")
