import sys

import socketio
import uvicorn
from fastapi import FastAPI

# import keylogger_server as kl
import src.server.app_process_server as ap
import src.server.directory_tree_server as dt
import src.server.live_screen_server as lss
import src.server.shutdown_logout_server as sl
import src.server.sys_info_server as sys_info

PORT = 5656

# Use this to register FastAPI routes
api = FastAPI()

# Use this to register Socket.IO events
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*", logger=True)

app = socketio.ASGIApp(sio, api)


# Register shutdown and logout events
sl.callbacks(sio)

# Register system info events
sys_info.callbacks(sio)

# Register app process events
ap.callbacks(sio)

# Register live screen events
lss.callbacks(sio)

# Register directory tree events
dt.callbacks(sio)

if "nt" in sys.builtin_module_names:
    import src.server.registry_server as rs

    # Register registry events
    rs.callbacks(sio)


@sio.on("QUIT")
async def quit(sid, data):
    await sio.disconnect(sid)


def main():
    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
