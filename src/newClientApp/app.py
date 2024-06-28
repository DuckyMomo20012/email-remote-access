import dearpygui.dearpygui as dpg
import socketio

from src.shared.pages.base import BasePage
from src.shared.pages.popup import PopupWindow


class App:
    sio: socketio.Client
    histories: list[BasePage]

    def __init__(self):
        self.sio = socketio.Client(logger=True)
        self.histories = []

        # NOTE: Register the callbacks
        self.callbacks()

    def __del__(self):
        self.sio.disconnect()

    def goto(self, route: str):
        try:
            from src.newClientApp.routes import routes

            page = routes.get(route)

            if page is None:
                raise ValueError(f"Route {route} is not found")

            # NOTE: Init page
            page = page()

            if len(self.histories) > 0:
                dpg.configure_item(self.histories[-1].tag, show=False)

            page.render()
            # NOTE: Tag can be re-assigned while rendering
            self.histories.append(page)

            dpg.set_primary_window(page.tag, True)
        except SystemError:
            print(
                "RuntimeError: Cannot set primary window. Please check if the window is"
                " created with self.tag"
            )
        except ValueError:
            print("ValueError: Route is not found")

    def back(self):
        if len(self.histories) > 1:
            prevPage = self.histories.pop()
            dpg.delete_item(prevPage.tag)
            dpg.configure_item(self.histories[-1].tag, show=True)

    def callbacks(self):
        @self.sio.event
        def connect():
            PopupWindow("Connected to the server!", "Connected")

        @self.sio.event
        def connect_error(data):
            PopupWindow("Cannot connect to the server!", "Disconnected")


app = App()


def main():
    dpg.create_context()
    dpg.create_viewport(title="Remote Control", width=800, height=600)

    with dpg.font_registry():  # noqa: SIM117
        # First argument ids the path to the .ttf or .otf file
        with dpg.font("assets/fonts/IBMPlexMono-Regular.ttf", 20) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Vietnamese)

    dpg.bind_font(default_font)

    app.goto("/connect")
    # app.goto("/")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
