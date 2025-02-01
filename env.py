from pprint import pprint
from typing import Literal, cast
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()


class Env(BaseModel):
    ENV: Literal["development", "production", "staging"] = Field(default="development")
    TELEGRAM_BOT_TOKEN: str
    MINI_APP_DEEPLINK: str
    API_BASE_URL: str
    API_KEY: str


# * RUNTIME ENVIRONMENT
_ENV = os.environ.get("ENV", "development")

RunTimeEnvLiteral = Literal["development", "production", "staging"]
VALID_RUNTIME_ENVS = ["development", "production", "staging"]
if _ENV not in VALID_RUNTIME_ENVS:
    raise ValueError(
        f"Invalid ENV value: {_ENV}, must be one of the following: development, production, staging"
    )
_ENV = cast(RunTimeEnvLiteral, _ENV)

# * TELEGRAM BOT TOKEN FROM BOTFATHER
_TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not _TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "Environment variables not complete: TELEGRAM_BOT_TOKEN is required"
    )

# * BASE URL FOR API SERVICE
_API_BASE_URL = os.environ.get("API_BASE_URL")

if not _API_BASE_URL:
    raise ValueError("Environment variables not complete: API_BASE_URL is required")


# * API KEY FOR API SERVICE AUTHENTICATION
_API_KEY = os.environ.get("API_KEY")
if not _API_KEY:
    raise ValueError("Environment variables not complete: API_KEY is required")


# * TELEGRAM BOT DEEP LINK USED FOR THE MINI APP (e.g. https://t.me/your_bot)
_MINI_APP_DEEPLINK = os.environ.get("MINI_APP_DEEPLINK")

if not _MINI_APP_DEEPLINK:
    raise ValueError(
        "Environment variables not complete: MINI_APP_DEEPLINK is required"
    )


env = Env(
    ENV=_ENV,
    TELEGRAM_BOT_TOKEN=_TELEGRAM_BOT_TOKEN,
    MINI_APP_DEEPLINK=_MINI_APP_DEEPLINK,
    API_BASE_URL=_API_BASE_URL,
    API_KEY=_API_KEY,
)

print("[env.py] Environment variables loaded successfully")
print("==============================================")
pprint(env.model_dump())
print("==============================================\n")
