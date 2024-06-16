import appdirs
import os
import json

class Config:
    def __init__(self, app_name: str, default_config: dict = {}) -> None:
        self.app_name = app_name
        self.config = LoadConfig(app_name, default_config)

    def Save(self):
        cfg_path = GetConfigPath(self.app_name)
        with open(cfg_path, "w") as f:
            json.dump(self.config, f, indent=4)

def GetConfigPath(app_name: str) -> str:

    config_dir = appdirs.user_config_dir(appname=app_name, appauthor="com.github.jakestanley")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "config.json")

def LoadConfig(app_name: str, default_config={}) -> dict:

    config_path = GetConfigPath(app_name)
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    else:
        return default_config