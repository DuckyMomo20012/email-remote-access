import uuid

import psutil
import socketio


def callbacks(sio: socketio.AsyncServer):
    @sio.on("SYS:info")
    def on_sys_info(sid, data):
        try:
            return {
                "macAddress": hex(uuid.getnode())[2:].upper(),
                "cpu": psutil.cpu_percent(),
                "memory": psutil.virtual_memory().percent,
            }, None
        except Exception:
            return None, {"message": "Error while fetching system information"}
