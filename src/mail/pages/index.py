from typing import Union

import dearpygui.dearpygui as dpg

from src.mail.pages.base import BasePage


class IndexPage(BasePage):
    def __init__(self, tag: Union[int, str] = "w_index"):
        super().__init__(tag)

    def render(self):
        with dpg.window(label="Mail Inbox", tag=self.tag, width=400, height=200):
            dpg.add_text("Hello World")
