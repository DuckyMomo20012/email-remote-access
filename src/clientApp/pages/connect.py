from typing import Union

import dearpygui.dearpygui as dpg
import socketio
import socketio.exceptions

from src.clientApp.app import app
from src.server.server import PORT
from src.shared.pages.base import BasePage


class ConnectPage(BasePage):
    def __init__(self, tag: Union[int, str] = "w_connect"):
        super().__init__(tag)

    def handleConnectClick(self):
        dpg.hide_item("t_status")

        ip = dpg.get_value("f_ip")

        if ip == "":
            dpg.show_item("t_status")
            dpg.set_value("t_status", "Please enter an IP address")
            return

        try:
            app.sio.connect(f"http://{ip}:{PORT}")

            app.goto("/")
        except socketio.exceptions.ConnectionError:
            dpg.show_item("t_status")
            dpg.set_value("t_status", "Cannot connect to the server")

    def render(self):
        with dpg.window(label="Connect to server", tag=self.tag, width=400, height=200):
            dpg.add_input_text(
                label="IP Address",
                tag="f_ip",
                hint="127.0.0.1",
                default_value="127.0.0.1",
            )

            # NOTE: A placeholder for the status text
            dpg.add_text(tag="t_status", show=False, color=[255, 0, 0])

            dpg.add_button(label="Connect", callback=self.handleConnectClick)
