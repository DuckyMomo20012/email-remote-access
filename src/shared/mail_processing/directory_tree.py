import os
import uuid

import socketio

from src.shared.mail_processing.utils import Command, sendMessage


def onListDirectoryMessage(
    service, sio: socketio.Client, cmd: Command, reqMessage, reply=True
):
    if not cmd["options"]:
        raise Exception("No path specified")

    path = cmd["options"]

    def handleDirectoryData(data: str, err):
        if err is not None:
            sendMessage(
                service,
                reqMessage,
                err["message"],
                reply=reply,
            )

        tmpTextFile = f"directory_{uuid.uuid4()}.txt"
        try:
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


def onCopyFileToServerMessage(
    service, sio: socketio.Client, cmd: Command, reqMessage, reply=True
):
    if not cmd["options"]:
        raise Exception("No file path or destination path specified")

    filePath, destPath = cmd["options"].split(";")

    if not filePath:
        raise Exception("No file path specified")

    if not os.path.exists(filePath):
        raise Exception(f'"{filePath}" file not found')

    def handleCopyFileStatus(data, err):
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
            f"Copy file {data} successfully!",
            reply=reply,
        )

    sio.emit(
        "DIRECTORY:send",
        {
            "fileName": os.path.basename(filePath),
            "destPath": destPath,
            "data": open(filePath, "rb").read(),  # noqa: SIM115
        },
        callback=handleCopyFileStatus,
    )


def onCopyFileToClientMessage(
    service, sio: socketio.Client, cmd: Command, reqMessage, reply=True
):
    if not cmd["options"]:
        raise Exception("No file path or destination path specified")

    filePath, destPath = cmd["options"].split(";")

    if not filePath:
        raise Exception("No file path specified")

    if not os.path.exists(filePath):
        raise Exception(f'"{filePath}" file not found')

    def handleReceiveFileData(data: dict, err):
        if err is not None:
            sendMessage(
                service,
                reqMessage,
                data["message"],
                reply=reply,
            )
            return

        try:
            with open(os.path.join(destPath, data["fileName"]), "wb") as f:
                f.write(data["data"])

            sendMessage(
                service,
                reqMessage,
                f'"{data["fileName"]}" file copied to client',
                reply=reply,
            )

        except Exception:
            sendMessage(
                service,
                reqMessage,
                f'Cannot write "{filePath}" file to client',
                reply=reply,
            )
            return

    sio.emit("DIRECTORY:receive", filePath, callback=handleReceiveFileData)


def onCopyFileToClientStreamMessage(
    service, sio: socketio.Client, cmd: Command, reqMessage, reply=True
):
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

    @sio.on("DIRECTORY:copy:stream:data")
    def handleReceiveFileData(data: dict):
        fileName = data["filename"]
        fileData = data["fileData"]

        with open(destPath + fileName, "ab") as f:
            f.write(fileData)
            # NOTE: Flush is needed to write data to file immediately
            f.flush()

    @sio.on("DIRECTORY:copy:stream:done")
    def handleReceiveFileDone(data):
        pass
        # sendMessage(
        #     service,
        #     reqMessage,
        #     f'"{filePath}" file copied to client',
        #     reply=reply,
        # )

    sio.emit("DIRECTORY:copy:stream", filePath)


def onCopyFileToServerStreamMessage(
    service, sio: socketio.Client, cmd: Command, reqMessage, reply=True
):
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

    @sio.on("DIRECTORY:copyto:stream:data")
    def handleReceiveFileData(data: dict):
        fileName = data["filename"]
        fileData = data["fileData"]

        with open(destPath + fileName, "ab") as f:
            f.write(fileData)
            # NOTE: Flush is needed to write data to file immediately
            f.flush()

    @sio.on("DIRECTORY:copyto:stream:done")
    def handleReceiveFileDone(data):
        sendMessage(
            service,
            reqMessage,
            f'"{filePath}" file copied to client',
            reply=reply,
        )

    sio.emit(
        "DIRECTORY:copyto:stream",
        {
            "metadata": f"{filePath}{SEPARATOR}{destPath}",
            "data": open(filePath, "rb").read(),
        },
    )


def onDeleteFileMessage(
    service, sio: socketio.Client, cmd: Command, reqMessage, reply=True
):
    if not cmd["options"]:
        raise Exception("No file path specified")
        return

    path = cmd["options"]

    def handleDeleteFileStatus(data, err):
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
            f"Delete file {data} successfully!",
            reply=reply,
        )

    sio.emit("DIRECTORY:delete", path, callback=handleDeleteFileStatus)
