import socketio

from src.shared.mail_processing.utils import Command, sendMessage


def onSysInfoMessage(
    service, sio: socketio.Client, cmd: Command, reqMessage, reply=True
):
    def handleSysInfoData(data, err):
        if err is not None:
            sendMessage(
                service,
                reqMessage,
                err["message"],
                reply=reply,
            )
            return

        sendMessage(
            service,
            reqMessage,
            f"Client {'\n'.join([
                f"MAC Address: {data['macAddress']}",
                f"CPU Usage: {data['cpu']}%",
                f"Memory Usage: {data['memory']}%"
            ])}",
            reply=reply,
        )

    sio.emit("SYS:info", "", callback=handleSysInfoData)
