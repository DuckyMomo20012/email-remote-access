import os
import struct

import psutil
import socketio


def send_data(client, data):
    size = struct.pack("!I", len(data))
    data = size + data
    client.sendall(data)
    return


def list_apps():
    ls1 = list()
    ls2 = list()
    ls3 = list()

    cmd = "powershell \"gps | where {$_.mainWindowTitle} \
        | select Description, ID, @{Name='ThreadCount';Expression ={$_.Threads.Count}}"
    proc = os.popen(cmd).read().split("\n")
    tmp = list()
    for line in proc:
        if not line.isspace():
            tmp.append(line)
    tmp = tmp[3:]
    for line in tmp:
        try:
            arr = line.split(" ")
            if len(arr) < 3:
                continue
            if arr[0] == "" or arr[0] == " ":
                continue

            name = arr[0]
            threads = arr[-1]
            ID = 0
            # interation
            cur = len(arr) - 2
            for i in range(cur, -1, -1):
                if len(arr[i]) != 0:
                    ID = arr[i]
                    cur = i
                    break
            for i in range(1, cur, 1):
                if len(arr[i]) != 0:
                    name += " " + arr[i]
            ls1.append(name)
            ls2.append(ID)
            ls3.append(threads)
        except Exception:
            pass
    return ls1, ls2, ls3


def list_processes():
    ls1 = list()
    ls2 = list()
    ls3 = list()
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            name = proc.name()
            pid = proc.pid
            threads = proc.num_threads()
            ls1.append(str(name))
            ls2.append(str(pid))
            ls3.append(str(threads))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return ls1, ls2, ls3


def kill(pid):
    cmd = "taskkill.exe /F /PID " + str(pid)
    try:
        a = os.system(cmd)
        if a == 0:
            return 1
        else:
            return 0
    except Exception:
        return 0


def start(name):
    os.system(name)
    return


def callbacks(sio: socketio.AsyncServer):
    @sio.on("APP_PRO:kill")
    async def on_proc_kill(sid, data):
        res = kill(data)
        await sio.emit("APP_PRO:kill:status", res)

    @sio.on("APP_PRO:list")
    async def on_proc_list(sid):
        ls1, ls2, ls3 = list_processes()
        await sio.emit("APP_PRO:list:status", [ls1, ls2, ls3])

    @sio.on("APP_PRO:list:app")
    async def on_app_list(sid):
        ls1, ls2, ls3 = list_apps()
        await sio.emit("APP_PRO:list:status", [ls1, ls2, ls3])

    @sio.on("APP_PRO:start")
    async def on_proc_start(sid, data):
        res = start(data)
        await sio.emit("APP_PRO:start:status", res)
