import dearpygui.dearpygui as dpg
import socketio
from google.oauth2.credentials import Credentials

from src.shared.pages.base import BasePage


class App:
    sio: socketio.Client
    histories: list[BasePage]
    creds: Credentials = None

    def __init__(self):
        self.sio = socketio.Client()
        self.histories = []

    def __del__(self):
        self.sio.disconnect()

        for page in self.histories:
            page.__del__()

    def goto(self, page: BasePage):
        if len(self.histories) > 0:
            dpg.configure_item(self.histories[-1].tag, show=False)
        page.render()
        # NOTE: Tag can be re-assigned while rendering
        self.histories.append(page)

        dpg.set_primary_window(page.tag, True)

    def back(self):
        if len(self.histories) > 1:
            prevPage = self.histories.pop()
            dpg.delete_item(prevPage.tag)
            dpg.configure_item(self.histories[-1].tag, show=True)


app = App()


def main():
    from src.mailApp.pages.connect import ConnectPage
    from src.mailApp.pages.oauth import OAuthPage

    dpg.create_context()
    dpg.create_viewport(title="Remote Control", width=800, height=600)

    with dpg.font_registry():
        # First argument ids the path to the .ttf or .otf file
        with dpg.font("assets/fonts/IBMPlexMono-Regular.ttf", 20) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Vietnamese)

    dpg.bind_font(default_font)

    app.goto(OAuthPage(redirect=ConnectPage))

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

    # NOTE: Have to call this manually so the program can exit after the window
    # is closed
    app.__del__()


if __name__ == "__main__":
    main()
