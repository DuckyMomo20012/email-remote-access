from typing import Union

import dearpygui.dearpygui as dpg
import socketio
from google.oauth2.credentials import Credentials

from src.mail.pages.base import BasePage


class App:
    sio: socketio.Client
    histories: list[Union[int, str]]
    creds: Credentials = None

    def __init__(self):
        self.sio = socketio.Client()
        self.histories = []

    def goto(self, page: BasePage):
        if len(self.histories) > 0:
            dpg.configure_item(self.histories[-1], show=False)
        page.render()
        # NOTE: Tag can be re-assigned while rendering
        self.histories.append(page.tag)

        dpg.set_primary_window(page.tag, True)

    def back(self):
        if len(self.histories) > 1:
            prevPage = self.histories.pop()
            dpg.delete_item(prevPage)
            dpg.configure_item(self.histories[-1], show=True)


app = App()


def main():
    from src.mail.pages.connect import ConnectPage
    from src.mail.pages.oauth import OAuthPage

    dpg.create_context()
    dpg.create_viewport(title="Remote Control", width=1280, height=800)

    app.goto(OAuthPage(redirect=ConnectPage))

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
