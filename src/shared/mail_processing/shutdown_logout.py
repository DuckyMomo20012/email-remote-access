import socketio

from src.shared.mail_processing.utils import Command, sendMessage


def onShutdownMessage(
    service, sio: socketio.Client, cmd: Command, reqMessage, reply=True
):
    sio.emit("SD_LO:shutdown", "")

    sendMessage(
        service,
        reqMessage,
        '"shutdown" command sent to client',
        reply=reply,
    )


def onLogoutMessage(
    service, sio: socketio.Client, cmd: Command, reqMessage, reply=True
):
    sio.emit("SD_LO:logout", "")

    sendMessage(
        service,
        reqMessage,
        '"logout" command sent to client',
        reply=reply,
    )
