import os
from typing import TypedDict

import psutil
import seedir
import socketio


class SendDataRequest(TypedDict):
    fileName: str
    destPath: str
    data: bytes

BUFSIZE = 1000 * 1000  # 1MB


def listDisk():
    disks = psutil.disk_partitions(all=False)

    return [disk.mountpoint for disk in disks], None


def listDir(path: str):
    try:
        if not os.path.isdir(path):
            return None, {"message": "Invalid path"}

        return [
            (dirName, os.path.isdir(os.path.join(path, dirName)))
            for dirName in os.listdir(path)
        ], None
    except PermissionError as err:
        return None, {"message": f"Permission Denied: {err}"}


def listDirPretty(path: str):
    try:
        if not os.path.isdir(path):
            return None, {"message": "Invalid path"}

        # NOTE: r is for raw string, to prevent invalid path
        tree_dir = seedir.seedir(rf"{path}", printout=False, style="emoji")

        return tree_dir, None
    except PermissionError as err:
        return None, {"message": f"Permission Denied: {err}"}


def writeFile(fileName: str, desPath: str, data: bytes):
    try:
        with open(os.path.join(desPath, fileName), "wb") as f:
            f.write(data)

            return fileName, None

    except OSError as err:
        return None, {"message": f"Cannot write file: {err}"}


def readFile(filePath: str):
    if not os.path.isfile(filePath):
        return None, {"message": "File not found"}

    try:
        with open(filePath, "rb") as f:
            data = f.read()
            return {"fileName": os.path.basename(filePath), "data": data}, None
    except OSError as err:
        return None, {"message": f"Cannot read file: {err}"}


def deleteFile(path: str):
    if not os.path.isfile(path):
        return None, {"message": "File not found"}

    try:
        os.remove(path)
        return os.path.basename(path), None

    except OSError as err:
        return None, {"message": f"Cannot delete file: {err}"}


def callbacks(sio: socketio.AsyncServer):
    @sio.on("DIRECTORY:list_disk")
    def on_show_tree(sid, data):
        return listDisk()

    @sio.on("DIRECTORY:list_dirs")
    def on_list_dirs(sid, path: str):
        return listDir(path)

    @sio.on("DIRECTORY:list_dirs:pretty")
    def on_list_dirs_pretty(sid, path: str):
        return listDirPretty(path)

    @sio.on("DIRECTORY:send")
    def on_dir_copyto(sid, data: SendDataRequest):
        return writeFile(data["fileName"], data["destPath"], data["data"])

    @sio.on("DIRECTORY:receive")
    def on_dir_copy(sid, filePath: str):
        return readFile(filePath)

    @sio.on("DIRECTORY:copy:stream")
    async def on_dir_copy_stream(sid, filePath: str):
        if not os.path.isfile(filePath):
            return {"msg": "File not found"}

        try:
            with open(filePath, "rb") as f:
                while True:
                    data = f.read(BUFSIZE)
                    if data == b"":
                        break
                    await sio.emit(
                        "DIRECTORY:copy:stream:data",
                        {"filename": os.path.basename(filePath), "fileData": data},
                        to=sid,
                    )
                    # NOTE: Delay to prevent from packet loss
                    await sio.sleep(0.5)
                await sio.emit("DIRECTORY:copy:stream:done", "")
            return {"msg": "OK"}
        except Exception:
            return {"msg": "Cannot copy file"}

    @sio.on("DIRECTORY:delete")
    def on_dir_delete(sid, filePath: str):
        return deleteFile(filePath)
