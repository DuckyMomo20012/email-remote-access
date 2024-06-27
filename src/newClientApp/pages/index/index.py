from typing import Union

import dearpygui.dearpygui as dpg

from src.newClientApp.pages.index.list_process import ListProcessWindow
from src.shared.pages.base import BasePage


class IndexPage(BasePage):
    def __init__(self, tag: Union[int, str] = "w_index"):
        super().__init__(tag)

    def render(self):
        with dpg.window(label="Home", tag=self.tag, width=400, height=200):
            with dpg.group(horizontal=True):
                dpg.add_text("IP Address")
                dpg.add_text("MAC Address")
                dpg.add_text("CPU")
                dpg.add_text("RAM")

            g_body = dpg.add_group(horizontal=True)

            # NOTE: Have to render within context, and MUST pass a parent to it
            def renderListProcess():
                ListProcessWindow(parent=w).render()

            with dpg.group(width=200, parent=g_body):
                dpg.add_button(
                    label="List process",
                    callback=renderListProcess,
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
