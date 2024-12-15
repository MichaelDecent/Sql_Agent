# config/settings.py
import os

def set_env(key: str, value: str = None) -> None:
    if key not in os.environ:
        os.environ[key] = value
