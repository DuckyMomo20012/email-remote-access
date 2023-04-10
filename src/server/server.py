import threading
import tkinter as tk

import socketio
import uvicorn
from fastapi import FastAPI

# import keylogger_server as kl
import src.server.app_process_server as ap
import src.server.directory_tree_server as dt
import src.server.live_screen_server as lss
import src.server.mac_address_server as mac
import src.server.registry_server as rs
import src.server.shutdown_logout_server as sl

BUFSIZ = 1024 * 4
PORT = 5656


class ServerApp:
    def __init__(self):
        self.main = tk.Tk()
        self.main.geometry("200x200")
        self.main.title("Server")
        self.main["bg"] = "plum1"

        self.start_btn = tk.Button(
            self.main,
            text="OPEN",
            width=10,
            height=2,
            fg="white",
            bg="IndianRed3",
            borderwidth=0,
            highlightthickness=0,
            command=self.connect,
            relief="flat",
        )
        self.start_btn.place(x=100, y=100, anchor="center")

    def start(self):
        print("Server is running...")
        self.main.mainloop()

    def connect(self):
        server = Server()

        t = threading.Thread(target=server.start_server)
        t.daemon = True
        t.start()

        self.start_btn["state"] = tk.DISABLED


class Server:
    def __init__(self):
        self.app = FastAPI()

        self.sio = socketio.AsyncServer(
            async_mode="asgi", cors_allowed_origins="*", logger=True
        )
        self.app = socketio.ASGIApp(self.sio)

        # NOTE: Register the callbacks
        self.callbacks()

    def start_server(self):
        uvicorn.run(self.app, host="0.0.0.0", port=PORT)

    def callbacks(self):
        @self.sio.on("KEYLOG:start")
        def keylogger(sid):
            # kl.keylog(self.sio)
            return

        @self.sio.on("SD_LO:start")
        def shutdown_logout(sid):
            sl.shutdown_logout(self.sio)
            return

        @self.sio.on("MAC:start")
        async def mac_address(sid):
            await mac.mac_address(self.sio)
            return

        @self.sio.on("APP_PRO:start")
        def app_process(sid):
            ap.app_process(self.sio)
            return

        @self.sio.on("LIVESCREEN:start")
        async def live_screen(sid):
            await lss.capture_screen(self.sio)
            return

        @self.sio.on("DIRECTORY:start")
        def directory_tree(sid):
            dt.directory(self.sio)
            return

        @self.sio.on("REGISTRY:start")
        def registry(sid):
            rs.registry(self.sio)
            return

        @self.sio.on("QUIT")
        def quit(sid):
            exit(1)
            return


###############################################################################


def main():
    ServerApp().start()


if __name__ == "__main__":
    main()
