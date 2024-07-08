from typing import Union

import dearpygui.dearpygui as dpg
from socketio.exceptions import ConnectionError

from src.mailApp.app import app
from src.shared.pages.base import BasePage
from src.shared.pages.error import ErrorWindow

PORT = 5656


class ConnectPage(BasePage):
    def __init__(self, tag: Union[int, str] = "w_auth"):
        super().__init__(tag)

    def handleConnectClick(self):
        try:
            ip = dpg.get_value("f_ip")
            port = dpg.get_value("f_port")

            dpg.configure_item("b_connect", enabled=False)
            dpg.configure_item("b_connect", label="Connecting...")

            app.sio.connect(f"http://{ip}:{port}")
            dpg.configure_item("b_connect", label="Connect")
            app.goto("/")

        except ConnectionError:
            dpg.configure_item("b_connect", enabled=True)
            dpg.configure_item("b_connect", label="Connect")
            ErrorWindow("Cannot connect to server")

    def render(self):
        with dpg.window(
            label="Connect to the server",
            tag=self.tag,
            width=400,
            height=200,
            no_close=True,
        ):
            dpg.add_input_text(
                tag="f_ip", label="IP", default_value="127.0.0.1", hint="127.0.0.1"
            )
            dpg.add_input_text(
                tag="f_port", label="Port", default_value=f"{PORT}", enabled=False
            )
            dpg.add_button(
                label="Connect",
                callback=self.handleConnectClick,
                tag="b_connect",
            )
