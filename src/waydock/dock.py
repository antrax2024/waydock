from ctypes import CDLL

CDLL("libgtk4-layer-shell.so")
import gi  # pyright: ignore # noqa

gi.require_version("Gtk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")

from gi.repository import Gtk  # pyright: ignore #noqa
from gi.repository import Gtk4LayerShell as LayerShell  # pyright: ignore #noqa

from waydock.config import WaydockConfig  # pyright: ignore # noqa
from waydock.constants import STYLE_FILE  # pyright: ignore # noqa
from waydock.util import printLog  # pyright: ignore # noqa


class DockApplication:
    def __init__(self, config: WaydockConfig):
        self.app = Gtk.Application(application_id="com.antrax.waydock")
        self.window = None
        self.config = config
        self.app.connect("activate", self.on_activate)

    def startGTK(self):
        printLog("Starting GTK main loop")
        self.window = Gtk.Window(application=self.app)
        printLog("window created, setting properties for waydock window instance: ")
        self.window.set_name("waydock")
        # Carregar CSS
        printLog("Setting up style with CSS path: " + STYLE_FILE)
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(f"{STYLE_FILE}")
        display = self.window.get_display()
        Gtk.StyleContext.add_provider_for_display(
            display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        printLog("CSS provider loaded")

        printLog(
            f"bar size to '{self.config.window.width}x{self.config.window.height}'"  # pyright: ignore # noqa
        )
        window.set_default_size(self.config.window.width, self.config.window.height)  # pyright: ignore # noqa

        printLog("Layer Shell initialized")
        LayerShell.init_for_window(self.window)
        LayerShell.set_layer(self.window, LayerShell.Layer.TOP)

        # Anchor
        # LayerShell.set_anchor(window, LayerShell.Edge.BOTTOM, True)
        LayerShell.set_anchor(self.window, self.config.window.anchor, True)  # pyright: ignore # noqa
        # margins
        LayerShell.set_margin(
            self.window,
            LayerShell.Edge.BOTTOM,
            self.config.window.margin_bottom,  # pyright: ignore # noqa
        )
        LayerShell.set_margin(
            self.window, LayerShell.Edge.TOP, self.config.window.margin_top
        )  # pyright: ignore # noqa

        self.mainBox = Gtk.CenterBox(orientation=Gtk.Orientation.HORIZONTAL)
        # faz com que todos os widgets filhos ocupem o mesmo espaço
        # horizontalmente
        printLog("Setting homogeneous to True for mainBox.")
        # mainBox.set_homogeneous(False)

        self.window.set_child(self.mainBox)

        # Enable Exclusive Zone
        LayerShell.auto_exclusive_zone_enable(self.window)

        printLog("Show the window with all widgets.")
        self.window.present()

    def on_activate(self, app):
        printLog("Estou activated! hummmm")

    def run(self):
        self.app.run(None)
