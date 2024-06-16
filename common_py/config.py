import appdirs
import os
import json

def GetConfigPath(app_name: str = None) -> str:

    config_dir = appdirs.user_config_dir(appname=app_name, appauthor="com.github.jakestanley")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "config.json")

def LoadConfig() -> dict:

    config_path = GetConfigPath()
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    else:
        return {}