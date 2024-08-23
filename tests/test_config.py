import unittest

from common_py.config import _DEFAULT_CONFIG_FILE_NAME, Config, _GetConfigPath, _IsAppNameValid

class ExampleConfig(Config):
    def __init__(self, property) -> None:
        super().__init__("common_py")
        self.property = property

    def _PrepareSave(self):
        self.config["property"] = self.property

    def _DefaultConfig(self):
        cfg: dict = {}
        cfg["property"] = ""
        return cfg

class TestConfig(unittest.TestCase):

    def test_GetTemporaryFolder(self):
        config = ExampleConfig("common_py")
        temp_folder = config.GetTemporaryFolder()
        self.assertIn("com.github.jakestanley.common_py", temp_folder)

    def test_GetTemporaryFolderWhenGitSlugSupplied(self):
        config = ExampleConfig("com.github.jakestanley.common_py")
        temp_folder = config.GetTemporaryFolder()
        self.assertIn("com.github.jakestanley.common_py", temp_folder)

    def test_GetConfigPath(self):
        config_path = _GetConfigPath("common_py", "config.json")
        expectContains = "com.github.jakestanley.common_py/config.json"
        self.assertIn(expectContains, config_path)

    def test_GetConfigPathWhenGitSlugSupplied(self):
        config_path = _GetConfigPath("com.github.jakestanley.common_py", "config.json")
        expectContains = "com.github.jakestanley.common_py/config.json"
        self.assertIn(expectContains, config_path)

    def test_IsAppNameInvalid(self):
        self.assertTrue(_IsAppNameValid("com.github.jakestanley.common_py"))
        self.assertFalse(_IsAppNameValid("com.github.jakestanley.common_py/"))
        self.assertFalse(_IsAppNameValid("com.apple.cheese"))
