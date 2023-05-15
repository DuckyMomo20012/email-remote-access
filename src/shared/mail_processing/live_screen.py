import os
import uuid

import socketio

from src.shared.mail_processing.utils import Command, sendMessage


def onScreenshotMessage(
    service, sio: socketio.Client, cmd: Command, reqMessage, reply=True
):
    def handleScreenshotData(data: bytes):
        try:
            tmpImgFile = f"screenshot_{uuid.uuid4()}.png"
            with open(tmpImgFile, "wb") as f:
                f.write(data)

            sendMessage(
                service,
                reqMessage,
                "Client Screenshot",
                attachments=[tmpImgFile],
                reply=reply,
            )

        except Exception as e:
            print(e)
        finally:
            os.remove(tmpImgFile)

    sio.emit("LIVESCREEN:screenshot", "", callback=handleScreenshotData)
