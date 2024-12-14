# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()


def set_env(key: str):
    if key not in os.environ:
        os.environ[key] = os.getenv(key)
