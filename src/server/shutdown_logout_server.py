import socketio


def callbacks(sio: socketio.AsyncServer):
    @sio.on("SD_LO:shutdown")
    def on_shutdown(sid, data):
        try:
            print("shutdown")
            # FIXME: Uncomment this line
            # os.system("shutdown -s -t 15")
        except Exception:
            return {"msg": "Error while shutting down"}

    @sio.on("SD_LO:logout")
    def on_logout(sid, data):
        try:
            print("logout")
            # FIXME: Uncomment this line
            # os.system("shutdown -l")
        except Exception:
            return {"msg": "Error while logging out"}
