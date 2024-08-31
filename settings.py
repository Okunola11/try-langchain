import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

OPEN_API_KEY = os.environ.get("OPENAI_API_KEY")

UPSTASH_VECTOR_REST_TOKEN = os.environ.get("UPSTASH_VECTOR_REST_TOKEN")
UPSTASH_VECTOR_REST_URL = os.environ.get("UPSTASH_VECTOR_REST_URL")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

API_ACCESS_KEY = os.environ.get("API_ACCESS_KEY")