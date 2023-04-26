import os

import psutil
import socketio


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


def kill(pid: str):
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
    def on_proc_kill(sid, pid: str):
        status = kill(pid)

        return status

    @sio.on("APP_PRO:list")
    def on_proc_list(sid, data):
        procNames, pids, threads = list_processes()

        return [procNames, pids, threads]

    @sio.on("APP_PRO:list:app")
    async def on_app_list(sid, data):
        appNames, pids, threads = list_apps()

        return [appNames, pids, threads]

    @sio.on("APP_PRO:start")
    async def on_proc_start(sid, name: str):
        status = start(name)

        return status
