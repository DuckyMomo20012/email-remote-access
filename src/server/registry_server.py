import re
import winreg
from binascii import hexlify

import socketio

regKeyList = [
    "HKEY_LOCAL_MACHINE",
    "HKEY_CURRENT_USER",
    "HKEY_CLASSES_ROOT",
    "HKEY_USERS",
]
regDataTypeList = [
    "REG_SZ",
    "REG_EXPAND_SZ",
    "REG_BINARY",
    "REG_DWORD",
    "REG_QWORD",
    "REG_MULTI_SZ",
]
# NOTE: Mapping data type string to constant int
regDataTypeMapping = dict(
    [[str(getattr(winreg, dataType)), dataType] for dataType in regDataTypeList]
)


def extractPath(path: str):
    # NOTE: Create a regex string that combines all the keys in regKeyMapping
    reKey = rf"{"|".join(regKeyList)}"
    keyType = re.match(reKey, path)
    if keyType is None:
        return None, None

    # NOTE: Extract the path from the full path and remove the first backslash
    subPath = re.sub(reKey, "", path).removeprefix("\\")

    return keyType.group(), subPath


def createKey(path: str):
    keyType, subPath = extractPath(path)
    if keyType is None:
        return None, {"message": "Invalid registry key"}

    winreg.CreateKey(getattr(winreg, keyType), subPath)

    return path, None


def deleteKey(path: str):
    keyType, subPath = extractPath(path)
    if keyType is None or subPath is None:
        return None, {"message": "Invalid registry key"}

    winreg.DeleteKey(getattr(winreg, keyType), subPath)

    return path, None


def getValue(path: str, valueName: str, expand=False):
    keyType, subPath = extractPath(path)
    if keyType is None or subPath is None:
        return None, {"message": "Invalid registry key"}

    try:
        key = winreg.OpenKey(getattr(winreg, keyType), subPath)
        value, dataType = winreg.QueryValueEx(key, valueName)

        # NOTE: REG_EXPAND_SZ case
        if regDataTypeMapping[str(dataType)] == "REG_EXPAND_SZ" and expand is True:
            value = winreg.ExpandEnvironmentStrings(value)

        return value, None
    except FileNotFoundError:
        return None, {"message": "Registry key not found"}


def setValue(path: str, valueName: str, dataType: str, value):
    keyType, subPath = extractPath(path)
    if keyType is None or subPath is None:
        return None, {"message": "Invalid registry key"}

    if dataType not in regDataTypeList:
        return None, {"message": "Invalid registry data type"}

    try:
        key = winreg.OpenKey(getattr(winreg, keyType), subPath, 0, winreg.KEY_WRITE)

        if dataType == "REG_BINARY":
            # NOTE: Convert string to hex then to bytes
            value = hexlify(value.encode())
        elif dataType == "REG_DWORD" or dataType == "REG_QWORD":
            value = int(value)
        elif dataType == "REG_MULTI_SZ":
            # Ref: https://stackoverflow.com/a/53396459/12512981
            value = list(value.split("\n"))

        winreg.SetValueEx(key, valueName, 0, getattr(winreg, dataType), value)

    except FileNotFoundError:
        return None, {"message": "Registry key not found"}
    except TypeError:
        return None, {"message": "Invalid registry data value"}
    except OverflowError:
        return None, {"message": "Data value is too large"}
    except ValueError:
        return None, {"message": "Invalid data value"}

    return path, None


def callbacks(sio: socketio.AsyncServer):
    @sio.on("REGISTRY:create_key")
    def create_key(sid, data):
        return createKey(data["path"])

    @sio.on("REGISTRY:delete_key")
    def delete_key(sid, data):
        return deleteKey(data["path"])

    @sio.on("REGISTRY:get_value")
    def get_value(sid, data):
        return getValue(data["path"], data["valueName"], data["expand"])

    @sio.on("REGISTRY:set_value")
    def set_value(sid, data):
        return setValue(
            data["path"], data["valueName"], data["dataType"], data["value"]
        )
