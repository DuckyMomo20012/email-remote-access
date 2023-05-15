import socketio

from src.shared.mail_processing.utils import Command, sendMessage


def onMacAddressMessage(
    service, sio: socketio.Client, cmd: Command, reqMessage, reply=True
):
    def handleMacData(address: str):
        sendMessage(
            service,
            reqMessage,
            f"Client MAC Address: {address}",
            reply=reply,
        )

    sio.emit("MAC:info", "", callback=handleMacData)
