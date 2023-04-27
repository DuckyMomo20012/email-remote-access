import os
import uuid

from src.server.directory_tree_server import SEPARATOR
from src.shared.mail_processing.utils import Command, sendMessage


def onListDirectoryMessage(service, sio, cmd: Command, reqMessage, reply=True):
    if not cmd["options"]:
        raise Exception("No path specified")
        return

    path = cmd["options"]

    def handleDirectoryData(data: str):
        try:
            tmpTextFile = f"directory_{uuid.uuid4()}.txt"
            with open(tmpTextFile, "wb") as f:
                f.write(data.encode("utf-8"))

            sendMessage(
                service,
                reqMessage,
                f'"{path}" directory',
                attachments=[tmpTextFile],
                reply=reply,
            )
        except Exception as e:
            print(e)
        finally:
            os.remove(tmpTextFile)

    sio.emit("DIRECTORY:list_dirs:pretty", path, callback=handleDirectoryData)


def onCopyFileToServerMessage(service, sio, cmd: Command, reqMessage, reply=True):
    if not cmd["options"]:
        raise Exception("No file path or destination path specified")
        return

    filePath, destPath = cmd["options"].split(";")

    if not filePath:
        raise Exception("No file path specified")
        return

    if not os.path.exists(filePath):
        raise Exception(f'"{filePath}" file not found')
        return

    def handleCopyFileStatus(status: str):
        if status == "OK":
            resMessage = f'"{filePath}" file copied to server'
        else:
            resMessage = f'Cannot copy "{filePath}" file to server'

        sendMessage(
            service,
            reqMessage,
            resMessage,
            reply=reply,
        )

    sio.emit(
        "DIRECTORY:copyto",
        {
            "metadata": f"{filePath}{SEPARATOR}{destPath}",
            "data": open(filePath, "rb").read(),
        },
        callback=handleCopyFileStatus,
    )


def onCopyFileToClientMessage(service, sio, cmd: Command, reqMessage, reply=True):
    if not cmd["options"]:
        raise Exception("No file path or destination path specified")
        return

    filePath, destPath = cmd["options"].split(";")

    if not filePath:
        raise Exception("No file path specified")
        return

    if not os.path.exists(filePath):
        raise Exception(f'"{filePath}" file not found')
        return

    def handleReceiveFileData(data: dict):
        if isinstance(data, dict) and "msg" in data:
            sendMessage(
                service,
                reqMessage,
                data["msg"],
                reply=reply,
            )
            return

        try:
            fileName = data["filename"]
            fileData = data["fileData"]

            with open(destPath + fileName, "wb") as f:
                f.write(fileData)
        except Exception:
            sendMessage(
                service,
                reqMessage,
                f'Cannot write "{filePath}" file to client',
                reply=reply,
            )
            return

    sio.emit("DIRECTORY:copy", filePath, callback=handleReceiveFileData)


def onDeleteFileMessage(service, sio, cmd: Command, reqMessage, reply=True):
    if not cmd["options"]:
        raise Exception("No file path specified")
        return

    path = cmd["options"]

    def handleDeleteFileStatus(status: str):
        if status == "OK":
            resMessage = f'"{path}" file deleted'
        else:
            resMessage = f'Cannot delete "{path}" file'

        sendMessage(
            service,
            reqMessage,
            resMessage,
            reply=reply,
        )

    sio.emit("DIRECTORY:delete", path, callback=handleDeleteFileStatus)
