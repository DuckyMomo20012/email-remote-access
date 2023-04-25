from typing import Callable, Optional, TypedDict, Union

import dearpygui.dearpygui as dpg
from socketio.exceptions import ConnectionError

from src.mail.app import app
from src.mail.pages.base import BasePage
from src.mail.pages.error import ErrorWindow
from src.mail.pages.index.index import IndexPage

PORT = 5656


class TConnectForm(TypedDict):
    ip: str
    port: int


class ConnectForm(BasePage):
    def __init__(
        self,
        tag: Union[int, str] = "w_connect_form",
        onSubmit: Optional[Callable[[TConnectForm], None]] = None,
    ):
        super().__init__(tag)
        self.onSubmit = onSubmit

    def handleSubmit(self, callback: Optional[Callable[[TConnectForm], None]] = None):
        ip = dpg.get_value("f_ip")
        port = dpg.get_value("f_port")
        if callback:
            callback({"ip": ip, "port": port})

    def render(self):
        with dpg.window(
            label="Connect to the server",
            tag=self.tag,
            width=400,
            height=200,
            no_close=True,
        ):
            dpg.add_input_text(tag="f_ip", label="IP", hint="127.0.0.1")
            dpg.add_input_text(
                tag="f_port", label="Port", default_value=f"{PORT}", enabled=False
            )
            dpg.add_button(
                label="Connect",
                callback=lambda: self.handleSubmit(self.onSubmit),
                tag="b_connect",
            )


class ConnectPage(BasePage):
    def __init__(self, tag: Union[int, str] = "w_auth"):
        super().__init__(tag)

    def connect(self, form: TConnectForm):
        try:
            dpg.configure_item("b_connect", enabled=False)
            dpg.configure_item("b_connect", label="Connecting...")

            app.sio.connect(f"http://{form['ip']}:{form['port']}")
            dpg.configure_item("b_connect", label="Connect")
            app.goto(IndexPage())

        except ConnectionError:
            dpg.configure_item("b_connect", enabled=True)
            dpg.configure_item("b_connect", label="Connect")
            ErrorWindow("Cannot connect to server")

    def render(self):
        connectForm = ConnectForm(onSubmit=self.connect)
        connectForm.render()
        self.tag = connectForm.tag
