from typing import Union

import dearpygui.dearpygui as dpg

from src.newClientApp.pages.index.list_process import ListProcessWindow
from src.shared.pages.base import BasePage

windows: dict[str, BasePage] = {
    "/proc": ListProcessWindow,
}


class IndexPage(BasePage):
    def __init__(self, tag: Union[int, str] = "w_index"):
        super().__init__(tag)
        self.prevWindow: Union[int, str] = ""
        self.prevButton: Union[int, str] = ""

    def assignWindow(self, route: str, parent: Union[int, str], sender):
        try:
            w = windows.get(route)

            if w is None:
                raise ValueError(f"Route {route} is not found")

            w = w(parent=parent)

            if self.prevWindow != "" and self.prevButton != "":
                dpg.configure_item(self.prevButton, enabled=True)
                dpg.delete_item(self.prevWindow)
            self.prevWindow = w.tag
            self.prevButton = sender
            dpg.configure_item(self.prevButton, enabled=False)

            w.render()

        except ValueError:
            print("ValueError: Route is not found")

    def render(self):
        with dpg.window(label="Home", tag=self.tag, width=400, height=200):
            with dpg.group(horizontal=True):
                dpg.add_text("IP Address")
                dpg.add_text("MAC Address")
                dpg.add_text("CPU")
                dpg.add_text("RAM")

            g_body = dpg.add_group(horizontal=True)

            with dpg.group(width=200, parent=g_body):
                dpg.add_button(
                    label="List process",
                    # NOTE: Have to render within context, and MUST pass a parent to it
                    callback=lambda sender: self.assignWindow(
                        "/proc", parent=w, sender=sender
                    ),
                )
                dpg.add_button(label="List directory")
                dpg.add_button(label="Registry")
                dpg.add_button(label="Live screen")
                dpg.add_button(label="Shut down")
                dpg.add_button(label="Logout")

            w = dpg.add_child_window(
                autosize_x=True,
                border=True,
                parent=g_body,
                horizontal_scrollbar=True,
            )
