import json

from dataclasses import dataclass
import json

@dataclass
class AppConfig:
    url: str
    user: str
    password: str

def load_config(file_path: str) -> AppConfig:
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return AppConfig(**data)
    except Exception as e:
        raise Exception(f"error loading config file: {e}")