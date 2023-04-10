import uuid

import socketio


def callbacks(sio: socketio.AsyncServer):
    @sio.on("MAC:info")
    async def on_mac_address_info(sid):
        await sio.emit(
            "MAC:info:data",
            bytes(hex(uuid.getnode()), "utf8"),
        )
