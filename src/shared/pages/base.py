import threading
from functools import partial
from typing import Optional, Union

import dearpygui.dearpygui as dpg


class BasePage:
    tag: Union[int, str]
    _isActive: bool
    lock: threading.Lock

    @property
    def isActive(self):
        return self._isActive

    @isActive.setter
    def isActive(self, value):
        self.lock.acquire()
        self._isActive = value
        self.lock.release()

    def __init__(self, tag: Optional[Union[int, str]] = None):
        self.lock = threading.Lock()
        self.isActive = True
        if tag is None:
            self.tag = dpg.generate_uuid()
        else:
            self.tag = tag
        # NOTE: Automatically bind render method to renderWrapper to check if
        # the page is active before rendering
        # Ref: https://stackoverflow.com/a/54662690/12512981
        self.render = partial(self._renderWrapper, self.render)

    def deActive(self):
        self.isActive = False

    def reload(self, isPrimary: bool = True):
        try:
            if dpg.does_item_exist(self.tag):
                dpg.delete_item(self.tag)
            self.render()
            if isPrimary:
                dpg.set_primary_window(self.tag, True)
        except SystemError:
            print(
                "RuntimeError: Cannot set primary window. Please check if the window is"
                " created with self.tag"
            )

    def _renderWrapper(self, render):
        if not self.isActive:
            return
        render()

    def render(self):
        dpg.add_window(label="Base Page", tag=self.tag)
