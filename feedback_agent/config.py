import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
DOTENV_PATH = ROOT_DIR / ".env"
load_dotenv(dotenv_path=DOTENV_PATH)

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError(
        "Environment variable MISTRAL_API_KEY is missing. "
        f"Expected it in process env or in {DOTENV_PATH}."
    )

LLM_CONFIG = {
    "config_list": [
        {
            "model": "mistral-small-latest",
            "api_key": MISTRAL_API_KEY,
            "api_type": "mistral",
        }
    ],
    "temperature": 0.2,
    "cache_seed": None,
    "timeout": 60,
}