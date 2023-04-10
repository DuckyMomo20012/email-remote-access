import os

import socketio


def callbacks(sio: socketio.AsyncServer):
    @sio.on("SD_LO:shutdown")
    def on_shutdown(sid):
        print("shutdown")
        # FIXME: Uncomment this line
        # os.system("shutdown -s -t 15")

    @sio.on("SD_LO:logout")
    def on_logout(sid):
        print("logout")
        # FIXME: Uncomment this line
        # os.system("shutdown -l")
