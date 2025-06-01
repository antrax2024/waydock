# Config File Classes and Functions
#
# This module defines the configuration structure for qtbar using confz.
# confz provides type validation and default values for configuration parameters.
#
from confz import BaseConfig, FileSource
from waydock.constants import CONFIG_FILE
from typing import Literal, Union, Optional, List


class ComponentConfig(BaseConfig):
    type: str


class CustomConfig(ComponentConfig):
    type: Literal["custom"]  # pyright: ignore # noqa
    icon: Optional[str] = None  # icon  nerd font or emoji
    text: Optional[str] = None  # text to display
    command: Optional[str] = None  # command to run
    css_id: Optional[str] = None  # css id for the component
    refresh: int = 1000  # refresh time in milliseconds


class DisksConfig(ComponentConfig):
    type: Literal["disks"]  # pyright: ignore # noqa
    icon: Optional[str] = None  # icon  nerd font or emoji
    text: Optional[str] = "disks"  # text to display
    disks: List[str] = ["/"]  # list with  mount points disk identifiers
    css_id: Optional[str] = "disks"  # css id for the component
    refresh: int = 5000  # refresh time in milliseconds


class RAMConfig(ComponentConfig):
    type: Literal["ram"]  # pyright: ignore # noqa
    icon: Optional[str] = None  # icon  nerd font or emoji
    text: Optional[str] = "ram"  # text to display
    css_id: Optional[str] = None  # css id for the component
    refresh: int = 1000  # refresh time in milliseconds


class SeparatorConfig(ComponentConfig):
    type: Literal["separator"]  # pyright: ignore # noqa
    character: Optional[str] = "|"  # icon  nerd font or emoji
    css_class: Optional[str] = "separator"  # css id for the component


class CPUConfig(ComponentConfig):
    type: Literal["cpu"]  # pyright: ignore # noqa
    icon: Optional[str] = None  # icon  nerd font or emoji
    text: Optional[str] = "cpu"  # text to display

    css_id: Optional[str] = None  # css id for the component
    refresh: int = 1000  # refresh time in milliseconds


class TrayIconManagerConfig(ComponentConfig):
    type: Literal["tray"]  # pyright: ignore # noqa
    spacing: Optional[int] = 10  # space between icons
    css_id: Optional[str] = None  # css id for the component


class AppSwitchConfig(ComponentConfig):
    type: Literal["appswitch"]  # pyright: ignore # noqa
    workspaces: int = 1  # number of workspaces to display windows
    css_id: Optional[str] = None  # css id for the component


class KernelConfig(ComponentConfig):
    type: Literal["kernel"]  # pyright: ignore # noqa
    icon: Optional[str] = None  # icon  nerd font or emoji
    command: Optional[str] = "uname -r"  # command to run
    css_id: Optional[str] = None  # css id for the component
    refresh: int = 60000  # refresh time in milliseconds


class WorkspacesConfig(ComponentConfig):
    type: Literal["workspaces"]  # pyright: ignore # noqa
    ids: List[str]  # list with workspaces identifiers
    css_id: Optional[str] = None  # css id for the component


class ClockConfig(ComponentConfig):
    type: Literal["clock"]  # pyright: ignore # noqa
    icon: Optional[str] = None  # nerd font or emoji
    format: Optional[str] = "%H:%M:%S"
    css_id: Optional[str] = None
    refresh: Optional[int] = 1000


ComponentUnion = Union[
    CustomConfig,
    DisksConfig,
    RAMConfig,
    SeparatorConfig,
    CPUConfig,
    TrayIconManagerConfig,
    AppSwitchConfig,
    KernelConfig,
    WorkspacesConfig,
    ClockConfig,
]


class ContainerConfig(BaseConfig):
    hor_spacing: int = 4  # horizontal spacing
    components: List[ComponentUnion] = []


class WindowConfig(BaseConfig):
    """
    Configuration class for window appearance settings.

    Attributes:
        width (int): The width of the window in pixels. Default: 400
        height (int): The height of the window in pixels. Default: 150
    """

    anchor: str
    margin_bottom: int
    margin_top: int
    width: int
    height: int

    left_container: ContainerConfig
    right_container: ContainerConfig


class waydockConfig(BaseConfig):
    """
    Main configuration class for qtbar.

    Attributes:
        window (WindowConfig): Window-specific configuration settings
    """

    CONFIG_SOURCES = FileSource(CONFIG_FILE)
    window: WindowConfig
