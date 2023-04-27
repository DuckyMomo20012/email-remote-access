import os
import uuid

import tabulate

from src.shared.mail_processing.utils import Command, sendMessage


def onListProcessMessage(service, sio, cmd: Command, reqMessage, reply=True):
    def handleProcessData(data: list[list]):
        [procName, procId, threadCount] = data

        processInfo = list(zip(procName, procId, threadCount))

        prettyTable = tabulate.tabulate(
            processInfo,
            headers=["Process name", "PID", "Threads"],
            tablefmt="grid",
        )

        try:
            tmpTextFile = f"process_{uuid.uuid4()}.txt"
            with open(tmpTextFile, "wb") as f:
                f.write(prettyTable.encode("utf-8"))

            sendMessage(
                service,
                reqMessage,
                "Client Process List",
                attachments=[tmpTextFile],
                reply=reply,
            )
        except Exception as e:
            print(e)
        finally:
            os.remove(tmpTextFile)

    sio.emit("APP_PRO:list", "", callback=handleProcessData)


def onListApplicationMessage(service, sio, cmd: Command, reqMessage, reply=True):
    def handleAppData(data: list[list]):
        [appName, procId, threadCount] = data

        appInfo = list(zip(appName, procId, threadCount))

        prettyTable = tabulate.tabulate(
            appInfo,
            headers=["App name", "PID", "Threads"],
            tablefmt="grid",
        )

        try:
            tmpTextFile = f"app_{uuid.uuid4()}.txt"
            with open(tmpTextFile, "wb") as f:
                f.write(prettyTable.encode("utf-8"))

            sendMessage(
                service,
                reqMessage,
                "Client Application List",
                attachments=[tmpTextFile],
                reply=reply,
            )
        except Exception as e:
            print(e)
        finally:
            os.remove(tmpTextFile)

    sio.emit("APP_PRO:list:app", "", callback=handleAppData)


def onKillProcessMessage(service, sio, cmd: Command, reqMessage, reply=True):
    if not cmd["options"]:
        raise Exception("No PID specified")
        return

    pid = cmd["options"]

    def handleKillStatus(status: bool):
        if status:
            sendMessage(
                service,
                reqMessage,
                f"Process with PID {pid} killed",
                reply=reply,
            )
        else:
            sendMessage(
                service,
                reqMessage,
                f"Process with PID {pid} not found",
                reply=reply,
            )

    sio.emit("APP_PRO:kill", pid, callback=handleKillStatus)
