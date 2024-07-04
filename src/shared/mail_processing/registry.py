import socketio

from src.shared.mail_processing.utils import Command, sendMessage


def onCreateRegKey(service, sio: socketio.Client, cmd: Command, reqMessage, reply=True):
    if not cmd["options"]:
        raise Exception("No registry key specified")
        return

    keyPath = cmd["options"]

    def handleCreateRegKeyData(data, err):
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
            f'Successfully created registry key: "{data}"',
            reply=reply,
        )

    sio.emit(
        "REGISTRY:create_key",
        {
            "path": keyPath,
        },
        callback=handleCreateRegKeyData,
    )


def onDeleteRegKey(service, sio: socketio.Client, cmd: Command, reqMessage, reply=True):
    if not cmd["options"]:
        raise Exception("No registry key specified")
        return

    keyPath = cmd["options"]

    def handleDeleteRegKeyData(data, err):
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
            f'Successfully deleted registry key: "{data}"',
            reply=reply,
        )

    sio.emit(
        "REGISTRY:delete_key",
        {
            "path": keyPath,
        },
        callback=handleDeleteRegKeyData,
    )


def onSetRegValue(service, sio: socketio.Client, cmd: Command, reqMessage, reply=True):
    if not cmd["options"]:
        raise Exception("No information specified")
        return

    keyPath, valName, valData, valType = cmd["options"].split(";")

    def handleSetRegValueData(data, err):
        if err is not None:
            sendMessage(
                service,
                reqMessage,
                err["message"],
                reply=reply,
            )
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

    sio.emit(
        "REGISTRY:set_value",
        {
            "path": keyPath,
            "valueName": valName,
            "dataType": valType,
            "value": valData,
        },
        callback=handleSetRegValueData,
    )


def onGetRegValue(service, sio: socketio.Client, cmd: Command, reqMessage, reply=True):
    if not cmd["options"]:
        raise Exception("No information specified")
        return

    keyPath, name = cmd["options"].split(";")

    def handleGetRegValueData(data, err):
        if err is not None:
            sendMessage(
                service,
                reqMessage,
                err["message"],
                reply=reply,
            )
            return

        resMessage = (
            "Successfully got registry value:\n"
            + f"Key: {keyPath}\nName: {name}\nValue: {data}"
        )

        sendMessage(
            service,
            reqMessage,
            resMessage,
            reply=reply,
        )

    sio.emit(
        "REGISTRY:get_value",
        {
            "path": keyPath,
            "valueName": name,
            "expand": False,
        },
        callback=handleGetRegValueData,
    )
