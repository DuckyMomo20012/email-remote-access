import json

import socketio

from src.shared.mail_processing.utils import Command, sendMessage


def onCreateRegKey(service, sio: socketio.Client, cmd: Command, reqMessage, reply=True):
    if not cmd["options"]:
        raise Exception("No registry key specified")
        return

    keyPath = cmd["options"]

    def handleCreateRegKeyData(data: tuple[str, str]):
        [status, message] = data

        if status == "0":
            raise Exception("Incorrect registry key specified")
            return

        sendMessage(
            service,
            reqMessage,
            f'Successfully created registry key: "{keyPath}"',
            reply=reply,
        )

    req = {
        "ID": 3,
        "path": keyPath,
        "name_value": "",
        "value": "",
        "v_type": "REG_SZ",
    }

    msg = bytes(json.dumps(req), encoding="utf-8")

    sio.emit(
        "REGISTRY:edit",
        msg,
        callback=handleCreateRegKeyData,
    )


def onDeleteRegKey(service, sio: socketio.Client, cmd: Command, reqMessage, reply=True):
    if not cmd["options"]:
        raise Exception("No registry key specified")
        return

    keyPath = cmd["options"]

    def handleDeleteRegKeyData(data: tuple[str, str]):
        [status, message] = data

        if status == "0":
            raise Exception("Incorrect registry key specified")
            return

        sendMessage(
            service,
            reqMessage,
            f'Successfully deleted registry key: "{keyPath}"',
            reply=reply,
        )

    req = {
        "ID": 4,
        "path": keyPath,
        "name_value": "",
        "value": "",
        "v_type": "",
    }

    msg = bytes(json.dumps(req), encoding="utf-8")

    sio.emit(
        "REGISTRY:edit",
        msg,
        callback=handleDeleteRegKeyData,
    )


def onSetRegValue(service, sio: socketio.Client, cmd: Command, reqMessage, reply=True):
    if not cmd["options"]:
        raise Exception("No information specified")
        return

    keyPath, valName, valData, valType = cmd["options"].split(";")

    def handleSetRegValueData(data: tuple[str, str]):
        [status, message] = data

        if status == "0":
            raise Exception("Incorrect information specified")
            return

        resMessage = (
            "Successfully set registry value:\n"
            + f"Key: {keyPath}\nName: {valName}\nValue: {valData}\nType: {valType}"
        )

        sendMessage(
            service,
            reqMessage,
            resMessage,
            reply=reply,
        )

    req = {
        "ID": 2,
        "path": keyPath,
        "name_value": valName,
        "value": valData,
        "v_type": valType,
    }

    msg = bytes(json.dumps(req), encoding="utf-8")

    sio.emit(
        "REGISTRY:edit",
        msg,
        callback=handleSetRegValueData,
    )


def onGetRegValue(service, sio: socketio.Client, cmd: Command, reqMessage, reply=True):
    if not cmd["options"]:
        raise Exception("No information specified")
        return

    keyPath, name = cmd["options"].split(";")

    def handleGetRegValueData(data: tuple[str, str]):
        [status, message] = data

        if status == "0":
            raise Exception("Incorrect information specified")
            return

        resMessage = (
            "Successfully got registry value:\n"
            + f"Key: {keyPath}\nName: {name}\nValue: {message}"
        )

        sendMessage(
            service,
            reqMessage,
            resMessage,
            reply=reply,
        )

    req = {
        "ID": 1,
        "path": keyPath,
        "name_value": name,
        "value": "",
        "v_type": "",
    }

    msg = bytes(json.dumps(req), encoding="utf-8")

    sio.emit(
        "REGISTRY:edit",
        msg,
        callback=handleGetRegValueData,
    )
