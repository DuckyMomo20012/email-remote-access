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

PORT = 5656

# Use this to register FastAPI routes
api = FastAPI()

# Use this to register Socket.IO events
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*", logger=True)

app = socketio.ASGIApp(sio, api)


# @api.get("/")
# async def index():
#     return "Hello World"


@sio.on("KEYLOG:start")
def keylogger(sid):
    # kl.keylog(sio)
    return


# Register shutdown and logout events
sl.callbacks(sio)

# Register MAC address events
mac.callbacks(sio)

# Register app process events
ap.callbacks(sio)

# Register live screen events
lss.callbacks(sio)

# Register directory tree events
dt.callbacks(sio)

# Register registry events
rs.callbacks(sio)


@sio.on("QUIT")
async def quit(sid, data):
    await sio.disconnect(sid)


def main():
    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
