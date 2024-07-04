import os
import uuid

import socketio
import tabulate

from src.shared.mail_processing.utils import Command, sendMessage


def onListProcessMessage(
    service, sio: socketio.Client, cmd: Command, reqMessage, reply=True
):
    def handleProcessData(data: list[dict], err):
        if err is not None:
            sendMessage(
                service,
                reqMessage,
                err["message"],
                reply=reply,
            )
            return

        prettyTable = tabulate.tabulate(
            [proc.values() for proc in data],
            headers=["Process name", "PID", "Threads", "CPU usage", "Memory usage"],
            tablefmt="grid",
        )

        tmpTextFile = f"process_{uuid.uuid4()}.txt"
        try:
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


def onListApplicationMessage(
    service, sio: socketio.Client, cmd: Command, reqMessage, reply=True
):
    def handleAppData(data: list[dict], err):
        if err is not None:
            sendMessage(service, reqMessage, err["message"], reply=reply)
            return

        prettyTable = tabulate.tabulate(
            [proc.values() for proc in data],
            headers=["App name", "PID", "Threads", "CPU usage", "Memory usage"],
            tablefmt="grid",
        )

        tmpTextFile = f"app_{uuid.uuid4()}.txt"
        try:
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


def onKillProcessMessage(
    service, sio: socketio.Client, cmd: Command, reqMessage, reply=True
):
    if not cmd["options"]:
        raise Exception("No PID specified")

    pid = cmd["options"]

    def handleKillStatus(data, err):
        if err is not None:
            sendMessage(service, reqMessage, err["message"], reply=reply)
            return

        sendMessage(
            service,
            reqMessage,
            f"Process with PID {data} killed",
            reply=reply,
        )

    sio.emit("APP_PRO:kill", pid, callback=handleKillStatus)
