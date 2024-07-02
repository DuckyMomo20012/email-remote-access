from typing import Union

import dearpygui.dearpygui as dpg

from src.newClientApp.app import app
from src.newClientApp.pages.index.list_dir import ListDirWindow
from src.newClientApp.pages.index.list_process import ListProcessWindow
from src.newClientApp.pages.index.live_screen import LiveScreenWindow
from src.newClientApp.pages.index.reg_editor import RegistryEditorWindow
from src.shared.pages.base import BasePage
from src.shared.pages.confirm import ConfirmWindow

windows: dict[str, BasePage] = {
    "/proc": ListProcessWindow,
    "/dir": ListDirWindow,
    "/reg_editor": RegistryEditorWindow,
    "/live_screen": LiveScreenWindow,
}


class IndexPage(BasePage):
    prevWindow: BasePage | None

    def __init__(self, tag: Union[int, str] = "w_index"):
        super().__init__(tag)
        self.prevWindow = None
        self.prevButton: Union[int, str] = ""

        self.fetchInfo()

    def assignWindow(self, route: str, parent: Union[int, str], sender):
        try:
            w = windows.get(route)

            if w is None:
                raise ValueError(f"Route {route} is not found")

            w = w(parent=parent)

            if self.prevWindow is not None and self.prevButton != "":
                dpg.configure_item(self.prevButton, enabled=True)
                if dpg.does_item_exist(self.prevWindow.tag):
                    dpg.delete_item(self.prevWindow.tag)
                self.prevWindow.deActive()
            self.prevWindow = w
            self.prevButton = sender
            dpg.configure_item(self.prevButton, enabled=False)

            w.render()

        except ValueError:
            print("ValueError: Route is not found")

    def fetchInfo(self):
        def handleMessage(data):
            dpg.set_value("mac_address", f"MAC Address: {data}")

        app.sio.emit("MAC:info", "", callback=handleMessage)

    def render(self):
        with dpg.window(label="Home", tag=self.tag, width=400, height=200):
            with dpg.group(horizontal=True):
                dpg.add_text(tag="mac_address")

            g_body = dpg.add_group(horizontal=True)

            with dpg.group(width=200, parent=g_body):
                dpg.add_button(
                    label="List process",
                    # NOTE: Have to render within context, and MUST pass a parent to it
                    callback=lambda sender: self.assignWindow(
                        "/proc", parent=w, sender=sender
                    ),
                )
                dpg.add_button(
                    label="List directory",
                    callback=lambda sender: self.assignWindow(
                        "/dir", parent=w, sender=sender
                    ),
                )
                dpg.add_button(
                    label="Registry",
                    callback=lambda sender: self.assignWindow(
                        "/reg_editor", parent=w, sender=sender
                    ),
                )
                dpg.add_button(
                    label="Live screen",
                    callback=lambda sender: self.assignWindow(
                        "/live_screen", parent=w, sender=sender
                    ),
                )
                dpg.add_button(
                    label="Shut down",
                    callback=lambda: ConfirmWindow(
                        "Are you sure?", lambda: app.sio.emit("shutdown")
                    ),
                )

                dpg.add_button(
                    label="Logout",
                    callback=lambda: ConfirmWindow(
                        "Are you sure?", lambda: app.sio.emit("logout")
                    ),
                )

            w = dpg.add_child_window(
                autosize_x=True,
                border=True,
                parent=g_body,
                horizontal_scrollbar=True,
            )