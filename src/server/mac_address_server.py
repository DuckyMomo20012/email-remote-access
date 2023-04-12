import uuid

import socketio


def callbacks(sio: socketio.AsyncServer):
    @sio.on("MAC:info")
    def on_mac_address_info(sid, data):
        return hex(uuid.getnode())
