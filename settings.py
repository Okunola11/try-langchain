import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

OPEN_API_KEY = os.environ.get("OPEN_API_KEY")