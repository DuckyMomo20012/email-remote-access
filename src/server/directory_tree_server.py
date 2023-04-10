import os

import socketio

SEPARATOR = "<SEPARATOR>"


def showTree():
    listD = []
    for c in range(ord("A"), ord("Z") + 1):
        path = chr(c) + ":\\"
        if os.path.isdir(path):
            listD.append(path)
    return listD


def listDirs(path):
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


def delFile(path):
    if os.path.exists(path):
        try:
            os.remove(path)
            return True
        except Exception:
            return False
    else:
        return False


# copy file from client to server
def copyFileToServer(metadata, data):
    [filename, filesize, path] = metadata.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    try:
        with open(path + filename, "wb") as f:
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


def directory(sio: socketio.AsyncServer):
    @sio.on("DIRECTORY:show_tree")
    async def show(sid):
        await sio.emit("DIRECTORY:show_tree:data", showTree())

    @sio.on("DIRECTORY:list_dirs")
    async def list_dirs(sid, data):
        [status, dirs] = listDirs(data)

        if status:
            await sio.emit("DIRECTORY:list_dirs:data", dirs)
        else:
            await sio.emit("DIRECTORY:list_dirs:error")

    @sio.on("DIRECTORY:copyto")
    async def copyto(sid, data):
        copyFileStatus = copyFileToServer(data["metadata"], data["data"])
        if copyFileStatus:
            await sio.emit("DIRECTORY:copyto:status", "OK")
        else:
            await sio.emit("DIRECTORY:copyto:status", "NOT OK")

    @sio.on("DIRECTORY:copy")
    async def copy(sid, data):
        [status, fileData] = copyFileToClient(data)
        if status:
            await sio.emit(
                "DIRECTORY:copy:data",
                {"filename": os.path.basename(data), "fileData": fileData},
            )
        else:
            await sio.emit("DIRECTORY:copy:error")

    @sio.on("DIRECTORY:delete")
    async def delete(sid, data):
        delStatus = delFile(data)
        if delStatus:
            await sio.emit("DIRECTORY:delete:status", "OK")
        else:
            await sio.emit("DIRECTORY:delete:status", "NOT OK")
