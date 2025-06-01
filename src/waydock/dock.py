from ctypes import CDLL

CDLL("libgtk4-layer-shell.so")
import gi  # noqa

gi.require_version("Gtk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")

from gi.repository import Gtk  # pyright: ignore #noqa
from gi.repository import Gtk4LayerShell as LayerShell  # pyright: ignore #noqa
from gi.repository import GLib  # pyright: ignore # noqa

from waydock.config import waydockConfig  # pyright: ignore # noqa
from waydock.constants import STYLE_FILE, ANCHOR  # pyright: ignore # noqa
from waydock.widgets import populateBox  # pyright: ignore # noqa
from waydock.util import printLog  # pyright: ignore # noqa


waydockConfig = None
components = []
index = 0


def createGtkBox(h_align: Gtk.Align) -> Gtk.Box:
    retValue = Gtk.Box(
        orientation=Gtk.Orientation.HORIZONTAL,
        spacing=waydockConfig.window.left_container.hor_spacing,  # pyright: ignore # noqa
    )
    retValue.set_halign(h_align)
    retValue.set_valign(Gtk.Align.CENTER)
    return retValue


def onActivate(app):
    printLog("on activate triggered")
    window = Gtk.Window(application=app)
    printLog("window created, setting properties for waydock window instance: ")
    window.set_name("waydock")
    # Carregar CSS
    printLog("Setting up style with CSS path: " + STYLE_FILE)
    css_provider = Gtk.CssProvider()
    css_provider.load_from_path(f"{STYLE_FILE}")
    display = window.get_display()
    Gtk.StyleContext.add_provider_for_display(
        display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    printLog("CSS provider loaded")

    printLog(
        f"bar size to '{waydockConfig.window.width}x{waydockConfig.window.height}'"  # pyright: ignore # noqa
    )
    window.set_default_size(waydockConfig.window.width, waydockConfig.window.height)  # pyright: ignore # noqa

    printLog("Layer Shell initialized")
    LayerShell.init_for_window(window)
    LayerShell.set_layer(window, LayerShell.Layer.TOP)

    # Anchor
    # LayerShell.set_anchor(window, LayerShell.Edge.BOTTOM, True)
    LayerShell.set_anchor(window, ANCHOR[waydockConfig.window.anchor], True)  # pyright: ignore # noqa
    # margins
    LayerShell.set_margin(
        window,
        LayerShell.Edge.BOTTOM,
        waydockConfig.window.margin_bottom,  # pyright: ignore # noqa
    )
    LayerShell.set_margin(window, LayerShell.Edge.TOP, waydockConfig.window.margin_top)  # pyright: ignore # noqa

    mainBox = Gtk.CenterBox(orientation=Gtk.Orientation.HORIZONTAL)
    # faz com que todos os widgets filhos ocupem o mesmo espaço
    # horizontalmente
    printLog("Setting homogeneous to True for mainBox.")
    # mainBox.set_homogeneous(False)

    window.set_child(mainBox)

    # Enable Exclusive Zone
    LayerShell.auto_exclusive_zone_enable(window)

    printLog("Creating leftGtkBox for window...")
    leftGtkBox = createGtkBox(Gtk.Align.START)

    printLog("Creating rightGtkBox for window...")
    rightGtkBox = createGtkBox(Gtk.Align.END)

    mainBox.set_start_widget(leftGtkBox)
    mainBox.set_end_widget(rightGtkBox)

    printLog("Populate boxes with widgets.")
    populateBox(leftGtkBox, waydockConfig.window.left_container.components)  # pyright: ignore # noqa
    populateBox(rightGtkBox, waydockConfig.window.right_container.components)  # pyright: ignore # noqa

    printLog("Show the window with all widgets.")
    window.present()


def runwaydock(config: waydockConfig) -> None:
    """
    waydock is a GTK4 Layer Shell bar for Hyprland.
    """
    printLog("Instantiate the config Class ")
    global waydockConfig
    waydockConfig = config

    # Create the application
    printLog("Create a new Application instance with 'com.antrax.waydock' as an id")
    app = Gtk.Application(application_id="com.antrax.waydock")
    printLog("Connect to the activate signal of the application")
    app.connect("activate", onActivate)
    printLog("Start the GTK main loop with 'app.run()'")
    app.run(None)
