import os

import socketio

BUFSIZ = 1024 * 4


def shutdown_logout(sio: socketio.AsyncServer):
    @sio.on("SD_LO:shutdown")
    def shutdown(sid):
        print("shutdown")
        # FIXME: Uncomment this line
        # os.system("shutdown -s -t 15")

    @sio.on("SD_LO:logout")
    def logout(sid):
        print("logout")
        # FIXME: Uncomment this line
        # os.system("shutdown -l")
