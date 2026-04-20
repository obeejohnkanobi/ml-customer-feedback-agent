import os
from dotenv import load_dotenv
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError("Environment variable MISTRAL_API_KEY is missing.")

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