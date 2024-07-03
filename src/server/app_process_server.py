import psutil
import pywinctl as pwc
import socketio


def listProcess():
    try:
        procList: list[dict] = []
        for proc in psutil.process_iter():
            procInfo = dict()
            with proc.oneshot():
                procInfo["name"] = proc.name()
                procInfo["id"] = proc.pid
                procInfo["threads"] = proc.num_threads()
                procInfo["cpu_percent"] = proc.cpu_percent()
                procInfo["memory_percent"] = proc.memory_percent()

            procList.append(procInfo)

        return procList, None
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None, {"message": "Error while fetching process list"}


def listApp():
    apps = pwc.getAllAppsNames()
    procs, err = listProcess()
    if err is not None:
        return None, err

    if procs is None:
        return None, {"message": "Error while fetching process list"}
    appList: list[dict] = []
    for proc in procs:
        if proc["name"] in apps:
            appList.append(proc)

    return appList, None


def killApp(pid: str):
    try:
        proc = psutil.Process(int(pid))

        proc.kill()

        return pid, None
    except ValueError:
        return None, {"message": "Invalid PID"}


def callbacks(sio: socketio.AsyncServer):
    @sio.on("APP_PRO:list")
    def on_proc_list(sid, data):
        return listProcess()

    @sio.on("APP_PRO:list:app")
    async def on_app_list(sid, data):
        return listApp()

    @sio.on("APP_PRO:kill")
    def on_proc_kill(sid, pid: str):
        return killApp(pid)
