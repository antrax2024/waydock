# Config File Classes and Functions
#
# This module defines the configuration structure for qtbar using confz.
# confz provides type validation and default values for configuration parameters.
#
from confz import BaseConfig, FileSource
from waydock.constants import CONFIG_FILE


class WindowConfig(BaseConfig):
    anchor: str
    margin_bottom: int
    margin_top: int
    width: int
    height: int


class waydockConfig(BaseConfig):
    CONFIG_SOURCES = FileSource(CONFIG_FILE)
    window: WindowConfig
