from multiprocessing import Process
from typing import Union

import dearpygui.dearpygui as dpg
import psutil

import src.server.server as server
from src.server.server import PORT
from src.shared.pages.base import BasePage


class IndexPage(BasePage):
    def __init__(self, tag: Union[int, str] = "w_index"):
        super().__init__(tag)

    def startServer(self):
        self.proc = Process(target=server.main, daemon=True)
        self.proc.start()

    def stopServer(self):
        try:
            pid = self.proc.pid
            parent = psutil.Process(pid)
            for child in parent.children(recursive=True):
                child.kill()

            self.proc.terminate()

            print("Server stopped")
        except Exception:
            pass

    def render(self):
        with dpg.window(label="Home", tag=self.tag):

            def handleStartServerClick(sender, app_data, user_data):
                self.startServer()

                dpg.set_value("t_status", f"Server is running on port {PORT}")

                dpg.configure_item(sender, show=False)
                dpg.configure_item("b_stop", show=True)

            def handleStopServerClick(sender, app_data, user_data):
                self.stopServer()

                dpg.set_value("t_status", "Server is not running")

                dpg.configure_item("b_start", show=True)
                dpg.configure_item(sender, show=False)

            dpg.add_text("Server is not running", tag="t_status")

            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Start server",
                    tag="b_start",
                    callback=handleStartServerClick,
                )
                dpg.add_button(
                    label="Stop server",
                    tag="b_stop",
                    callback=handleStopServerClick,
                    show=False,
                )
