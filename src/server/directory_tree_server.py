import os

import seedir
import socketio

SEPARATOR = "<SEPARATOR>"


def showTree():
    listD = []
    for c in range(ord("A"), ord("Z") + 1):
        path = chr(c) + ":\\"
        if os.path.isdir(path):
            listD.append(path)
    return listD


def listDirs(path: str):
    if not os.path.isdir(path):
        return [False, path]

    try:
        listT = []
        listD = os.listdir(path)
        for d in listD:
            listT.append((d, os.path.isdir(path + "\\" + d)))

        return [True, listT]
    except Exception:
        return [False, None]


def delFile(path: str):
    if os.path.exists(path):
        try:
            os.remove(path)
            return True
        except Exception:
            return False
    else:
        return False


# copy file from client to server
def copyFileToServer(metadata: str, data: bytes):
    [filePath, destPath] = metadata.split(SEPARATOR)
    filename = os.path.basename(filePath)
    try:
        with open(destPath + filename, "wb") as f:
            f.write(data)
        return True
    except Exception:
        return False


# copy file from server to client
def copyFileToClient(filename):
    if not os.path.isfile(filename):
        return [False, None]
    with open(filename, "rb") as f:
        data = f.read()
        return [True, data]


def callbacks(sio: socketio.AsyncServer):
    @sio.on("DIRECTORY:show_tree")
    def on_show_tree(sid, data):
        return showTree()

    @sio.on("DIRECTORY:list_dirs")
    def on_list_dirs(sid, path: str):
        [status, dirs] = listDirs(path)

        if status:
            return dirs
        else:
            return {"msg": "Directory not found"}

    @sio.on("DIRECTORY:list_dirs:pretty")
    async def on_list_dirs_pretty(sid, path: str):
        try:
            # NOTE: r is for raw string, to prevent invalid path
            tree_dir = seedir.seedir(rf"{path}", printout=False, style="emoji")

            return tree_dir
        except PermissionError:
            return {"msg": "Permission Denied"}

    @sio.on("DIRECTORY:copyto")
    def on_dir_copyto(sid, data: dict):
        copyFileStatus = copyFileToServer(data["metadata"], data["data"])
        if copyFileStatus:
            return "OK"
        else:
            return "NOT OK"

    @sio.on("DIRECTORY:copy")
    def on_dir_copy(sid, filePath: str):
        [status, fileData] = copyFileToClient(filePath)
        if status:
            return {"filename": os.path.basename(filePath), "fileData": fileData}
        else:
            return {"msg": "Cannot copy file"}

    @sio.on("DIRECTORY:delete")
    def on_dir_delete(sid, filePath: str):
        delStatus = delFile(filePath)
        if delStatus:
            return "OK"
        else:
            return "NOT OK"
