from typing import Optional, Union

import dearpygui.dearpygui as dpg


class BasePage:
    tag: Union[int, str]

    def __init__(self, tag: Optional[Union[int, str]] = None):
        if tag is None:
            self.tag = dpg.generate_uuid()
        else:
            self.tag = tag

    def render(self):
        dpg.add_window(label="Base Page", tag=self.tag)
