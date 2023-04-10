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

app = FastAPI()

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*", logger=True)

app = socketio.ASGIApp(sio)


@sio.on("KEYLOG:start")
def keylogger(sid):
    # kl.keylog(sio)
    return


@sio.on("SD_LO:start")
def shutdown_logout(sid):
    sl.shutdown_logout(sio)
    return


@sio.on("MAC:start")
async def mac_address(sid):
    await mac.mac_address(sio)
    return


@sio.on("APP_PRO:start")
def app_process(sid):
    ap.app_process(sio)
    return


@sio.on("LIVESCREEN:start")
async def live_screen(sid):
    await lss.capture_screen(sio)
    return


@sio.on("DIRECTORY:start")
def directory_tree(sid):
    dt.directory(sio)
    return


@sio.on("REGISTRY:start")
def registry(sid):
    rs.registry(sio)
    return


@sio.on("QUIT")
def quit(sid):
    exit(1)
    return


def main():
    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
