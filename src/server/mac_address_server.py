import uuid

import socketio


def callbacks(sio: socketio.AsyncServer):
    @sio.on("MAC:info")
    def on_mac_address_info(sid, data):
        address = hex(uuid.getnode())
        address = address[2:].upper()
        address = ":".join(address[i : i + 2] for i in range(0, len(address), 2))

        return address
