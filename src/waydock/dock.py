# -*- coding: utf-8 -*-
"""
Dock for Wayland using GTK4 Layer Shell
Positioned at the bottom of the screen
"""

from ctypes import CDLL


# Load the GTK4 LayerShell library before importing gi
CDLL("libgtk4-layer-shell.so")
import gi
import sys
import subprocess
import os

# Check if required versions are available
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gio", "2.0")

try:
    gi.require_version("LayerShell", "1.0")
except ValueError:
    print("ERROR: GTK4 Layer Shell is not installed.")
    print("To install on Arch Linux: sudo pacman -S gtk4-layer-shell")
    print("To install on Ubuntu/Debian: sudo apt install libgtk4-layer-shell0")
    sys.exit(1)

from gi.repository import LayerShell as LayerShell  # pyright: ignore #noqa
from gi.repository import Gtk, Gdk, GdkPixbuf  # pyright: ignore # noqa


class DockApplication:
    def __init__(self):
        self.app = Gtk.Application(application_id="com.antrax.waydock")
        self.app.connect("activate", self.on_activate)
        self.window = None
        self.dock_box = None
        self.applications = []

    def on_activate(self, app):
        self.create_dock_window()
        self.populate_dock()
        self.window.present()  # pyright: ignore # noqa

    def create_dock_window(self):
        """Creates the main dock window"""
        self.window = Gtk.ApplicationWindow(application=self.app)
        self.window.set_title("WayDock")

        # Initialize Layer Shell
        LayerShell.init_for_window(self.window)

        # Configure layer shell - position at bottom
        LayerShell.set_layer(self.window, LayerShell.Layer.TOP)
        LayerShell.set_anchor(self.window, LayerShell.Edge.BOTTOM, True)
        LayerShell.set_anchor(self.window, LayerShell.Edge.LEFT, True)
        LayerShell.set_anchor(self.window, LayerShell.Edge.RIGHT, True)

        # Configure exclusive zone (reserve screen space)
        LayerShell.auto_exclusive_zone_enable(self.window)

        # Configure margins
        LayerShell.set_margin(self.window, LayerShell.Edge.BOTTOM, 0)
        LayerShell.set_margin(self.window, LayerShell.Edge.LEFT, 0)
        LayerShell.set_margin(self.window, LayerShell.Edge.RIGHT, 0)

        # Configure window styling
        self.setup_styling()

        # Create main container
        self.dock_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.dock_box.set_halign(Gtk.Align.CENTER)
        self.dock_box.set_valign(Gtk.Align.CENTER)
        self.dock_box.set_spacing(8)
        self.dock_box.set_margin_top(8)
        self.dock_box.set_margin_bottom(8)
        self.dock_box.set_margin_start(16)
        self.dock_box.set_margin_end(16)

        self.window.set_child(self.dock_box)

    def setup_styling(self):
        """Configure dock CSS styling"""
        css_provider = Gtk.CssProvider()
        css_data = """
        window {
            background-color: rgba(30, 30, 30, 0.9);
            border-radius: 12px;
        }

        .dock-button {
            background-color: rgba(255, 255, 255, 0.1);
            border: none;
            border-radius: 8px;
            padding: 8px;
            margin: 2px;
            transition: all 200ms ease;
        }

        .dock-button:hover {
            background-color: rgba(255, 255, 255, 0.2);
            transform: scale(1.1);
        }

        .dock-button:active {
            background-color: rgba(255, 255, 255, 0.3);
        }
        """

        css_provider.load_from_data(css_data.encode())
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),  # pyright: ignore # noqa
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def get_desktop_applications(self):
        """Fetches installed system applications"""
        apps = []
        desktop_dirs = [
            "/usr/share/applications",
            "/usr/local/share/applications",
            os.path.expanduser("~/.local/share/applications"),
        ]

        for desktop_dir in desktop_dirs:
            if os.path.exists(desktop_dir):
                for file in os.listdir(desktop_dir):
                    if file.endswith(".desktop"):
                        app_info = self.parse_desktop_file(
                            os.path.join(desktop_dir, file)
                        )
                        if app_info and not app_info.get("NoDisplay", False):
                            apps.append(app_info)

        # Filter main applications and sort by name
        main_apps = [app for app in apps if not app.get("NoDisplay", False)]
        main_apps.sort(key=lambda x: x.get("Name", "").lower())

        return main_apps[:10]  # Limit to 10 main applications

    def parse_desktop_file(self, filepath):
        """Parses .desktop file"""
        try:
            app_info = {}
            with open(filepath, "r", encoding="utf-8") as f:
                in_desktop_entry = False
                for line in f:
                    line = line.strip()
                    if line == "[Desktop Entry]":
                        in_desktop_entry = True
                        continue
                    elif line.startswith("[") and line.endswith("]"):
                        in_desktop_entry = False
                        continue

                    if in_desktop_entry and "=" in line:
                        key, value = line.split("=", 1)
                        app_info[key] = value

            # Check if valid application
            if app_info.get("Type") == "Application" and app_info.get("Exec"):
                return app_info
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

        return None

    def create_app_button(self, app_info):
        """Creates an application button"""
        button = Gtk.Button()
        button.add_css_class("dock-button")

        # Container for icon and tooltip
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_spacing(4)

        # Try to load icon
        icon_name = app_info.get("Icon", "application-x-executable")
        icon_size = 48

        try:
            # Try to load theme icon
            icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())  # pyright: ignore # noqa

            if os.path.isabs(icon_name):
                # Absolute path icon
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    icon_name, icon_size, icon_size, True
                )
                texture = Gdk.Texture.new_for_pixbuf(pixbuf)  # pyright: ignore # noqa
                icon = Gtk.Image.new_from_paintable(texture)
            else:
                # Theme icon
                icon = Gtk.Image.new_from_icon_name(icon_name)
                icon.set_pixel_size(icon_size)

        except Exception:
            # Fallback to default icon
            icon = Gtk.Image.new_from_icon_name("application-x-executable")
            icon.set_pixel_size(icon_size)

        box.append(icon)
        button.set_child(box)

        # Configure tooltip
        app_name = app_info.get("Name", "Application")
        button.set_tooltip_text(app_name)

        # Connect click event
        command = app_info.get("Exec", "")
        button.connect("clicked", self.launch_application, command)

        return button

    def launch_application(self, button, command):
        """Launches an application"""
        try:
            # Clean Exec field variables from .desktop
            command = (
                command.replace("%F", "")
                .replace("%f", "")
                .replace("%U", "")
                .replace("%u", "")
            )
            command = command.strip()

            # Run application in background
            subprocess.Popen(command, shell=True, start_new_session=True)
            print(f"Launching application: {command}")

        except Exception as e:
            print(f"Error launching application {command}: {e}")

    def add_separator(self):
        """Adds a visual separator"""
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        separator.set_margin_top(8)
        separator.set_margin_bottom(8)
        return separator

    def create_system_buttons(self):
        """Creates system buttons (applications menu, settings, etc.)"""
        buttons = []

        # Applications menu button
        menu_button = Gtk.Button()
        menu_button.add_css_class("dock-button")
        menu_icon = Gtk.Image.new_from_icon_name("view-app-grid-symbolic")
        menu_icon.set_pixel_size(32)
        menu_button.set_child(menu_icon)
        menu_button.set_tooltip_text("Applications Menu")
        # TODO: Implement popup menu
        buttons.append(menu_button)

        # Settings button
        settings_button = Gtk.Button()
        settings_button.add_css_class("dock-button")
        settings_icon = Gtk.Image.new_from_icon_name("preferences-system-symbolic")
        settings_icon.set_pixel_size(32)
        settings_button.set_child(settings_icon)
        settings_button.set_tooltip_text("Settings")
        settings_button.connect(
            "clicked", self.launch_application, "gnome-control-center"
        )
        buttons.append(settings_button)

        return buttons

    def populate_dock(self):
        """Populates dock with applications and system buttons"""
        # Add system buttons at the beginning
        system_buttons = self.create_system_buttons()
        for button in system_buttons:
            self.dock_box.append(button)  # pyright: ignore # noqa

        # Add separator
        self.dock_box.append(self.add_separator())  # pyright: ignore # noqa

        # Find and add main applications
        apps = self.get_desktop_applications()

        # Default apps if none found
        if not apps:
            default_apps = [
                {
                    "Name": "Terminal",
                    "Icon": "utilities-terminal",
                    "Exec": "gnome-terminal",
                },
                {"Name": "Web Browser", "Icon": "web-browser", "Exec": "firefox"},
                {"Name": "Text Editor", "Icon": "text-editor", "Exec": "gedit"},
                {"Name": "Files", "Icon": "system-file-manager", "Exec": "nautilus"},
            ]
            apps = default_apps

        for app in apps:
            button = self.create_app_button(app)
            self.dock_box.append(button)  # pyright: ignore # noqa

    def run(self):
        """Runs the application"""
        return self.app.run(sys.argv)


def main():
    """Main function"""
    print("Starting Wayland Dock...")

    # Check if running on Wayland
    if os.environ.get("XDG_SESSION_TYPE") != "wayland":
        print("WARNING: This application was designed for Wayland.")
        print("Current session:", os.environ.get("XDG_SESSION_TYPE", "unknown"))

    dock = DockApplication()
    return dock.run()


if __name__ == "__main__":
    sys.exit(main())
