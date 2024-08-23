import appdirs
import os
import json

from abc import ABC, abstractmethod

_DEFAULT_CONFIG_FILE_NAME = "config.json"

class Config(ABC):
    def __init__(self, app_name: str, config_name: str = _DEFAULT_CONFIG_FILE_NAME) -> None:
        self.app_name = app_name
        self.config_name = config_name
        self.config = _LoadConfig(self.app_name, self.config_name, self._DefaultConfig())

    @abstractmethod
    def _DefaultConfig(self):
        pass

    @abstractmethod
    def _PrepareSave(self):
        pass

    def Save(self):
        # instruct the child class to prepare self.config for saving
        self._PrepareSave()
        # Save config to file
        cfg_path = _GetConfigPath(self.app_name, self.config_name)
        with open(cfg_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def GetTemporaryFolder(self):
        # add the slug if it's not provided
        if ("com.github.jakestanley." in self.app_name) == False:
            app_name = f"com.github.jakestanley.{self.app_name}"
        return appdirs.user_cache_dir(app_name, self.app_name)

def _IsAppNameValid(app_name: str) -> bool:

    # if we're trying to use a forbidden character, we're bad
    # NOTE: this is NOT a comprehensive safety check
    if "/" in app_name:
        return False

    # if appname contains my git repo slug, we're good
    if "com.github.jakestanley." in app_name:
        return True

    # if we're trying to use a different group, we're bad
    # NOTE: this is NOT a comprehensive safety check
    if "." in app_name:
        return False
    
    return True

def _GetConfigPath(app_name: str, config_name: str) -> str:

    if not _IsAppNameValid(app_name):
        raise Exception("Invalid app_name")

    # add the slug if it's not provided
    if ("com.github.jakestanley." in app_name) == False:
        app_name = f"com.github.jakestanley.{app_name}"

    config_dir = appdirs.user_config_dir(appname=app_name, appauthor="com.github.jakestanley")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, config_name)

def _LoadConfig(app_name: str, config_name: str, default_config={}) -> dict:

    config_path = _GetConfigPath(app_name, config_name)
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    else:
        return default_config
