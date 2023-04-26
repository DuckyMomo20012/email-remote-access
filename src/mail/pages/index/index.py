import base64
import email
import os
import re
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Literal, Optional, TypedDict, Union, cast

import dearpygui.dearpygui as dpg
import tabulate
from googleapiclient.discovery import build

from src.mail.app import app
from src.mail.pages.base import BasePage
from src.mail.pages.error import ErrorWindow
from src.server.directory_tree_server import SEPARATOR
from src.utils.mail import composeMail, parseMail


class Command(TypedDict):
    type: Literal[
        "shutdown",
        "logout",
        "mac_address",
        "screenshot",
        "list_directory",
        "copy_file_to_server",
        "copy_file_to_client",
        "delete_file",
        "list_process",
        "list_application",
        "kill_process",
    ]
    options: Optional[str]


DEFAULT_COMMANDS = [
    "shutdown",
    "logout",
    "mac_address",
    "screenshot",
    "list_directory",
    "copy_file_to_server",
    "copy_file_to_client",
    "delete_file",
    "list_process",
    "list_application",
    "kill_process",
]


def parseCmd(msg: str) -> list[Command]:
    # NOTE: The pattern was not intentionally escaped to join the commands with
    # `|`
    cmdPattern = "|".join(DEFAULT_COMMANDS)

    # NOTE: We limit the options to only alphanumeric and `\\` and `:` to
    # increase the matching accuracy. The `\\` and `:` was included in the
    # options for the file path
    pattern = rf"\((?P<type>{cmdPattern})(?:\:(?P<options>[\w\\:]*))?\)"

    result = re.finditer(pattern, msg)

    cmds: list[Command] = []

    for match in result:
        type, options = match.group("type", "options")

        cmds.append(
            cast(
                Command,
                {
                    "type": type,
                    "options": options,
                },
            )
        )

    return cmds


# NOTE: This acts as a wrapper as we have to prepare some metadata before
# sending the message
def sendMessage(service, reqMessage, body, attachments=[], reply=True):
    userInfo = service.users().getProfile(userId="me").execute()

    fromUser = userInfo["emailAddress"]

    parsedReq = email.message_from_bytes(base64.urlsafe_b64decode(reqMessage["raw"]))

    toUser = parsedReq["From"]

    subject = f"{parsedReq['Subject']}"
    if reply:
        subject = f"Re: {subject}"

    message = composeMail(fromUser, toUser, subject, body, attachments)

    if reply:
        message["References"] = reqMessage["threadId"]
        message["In-Reply-To"] = reqMessage["threadId"]

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    if reply:
        create_message = {
            "raw": encoded_message,
            "threadId": reqMessage["threadId"],
        }
    else:
        create_message = {"raw": encoded_message}

    service.users().messages().send(userId="me", body=create_message).execute()


# REVIEW: This is a bit messy, we should refactor this later
def runCmd(service, sio, cmd: Command, reqMessage):
    if cmd["type"] == "shutdown":
        sio.emit("SD_LO:shutdown", "")

        sendMessage(service, reqMessage, '"shutdown" command sent to client')
    elif cmd["type"] == "logout":
        sio.emit("SD_LO:logout", "")

        sendMessage(service, reqMessage, '"logout" command sent to client')
    elif cmd["type"] == "mac_address":

        def handleMacData(address: str):
            sendMessage(
                service,
                reqMessage,
                f"Client MAC Address: {address}",
            )

        sio.emit("MAC:info", "", callback=handleMacData)
    elif cmd["type"] == "screenshot":

        def handleScreenshotData(data: bytes):
            try:
                tmpImgFile = f"screenshot_{uuid.uuid4()}.png"
                with open(tmpImgFile, "wb") as f:
                    f.write(data)

                sendMessage(
                    service,
                    reqMessage,
                    "Client Screenshot",
                    attachments=[tmpImgFile],
                )

            except Exception as e:
                print(e)
            finally:
                os.remove(tmpImgFile)

        sio.emit("LIVESCREEN:screenshot", "", callback=handleScreenshotData)
    elif cmd["type"] == "list_directory":
        if not cmd["options"]:
            ErrorWindow("No path specified")
            return

        path = cmd["options"]

        def handleDirectoryData(data: str):
            try:
                tmpTextFile = f"directory_{uuid.uuid4()}.txt"
                with open(tmpTextFile, "wb") as f:
                    f.write(data.encode("utf-8"))

                sendMessage(
                    service,
                    reqMessage,
                    f'"{path}" directory',
                    attachments=[tmpTextFile],
                )
            except Exception as e:
                print(e)
            finally:
                os.remove(tmpTextFile)

        sio.emit("DIRECTORY:list_dirs:pretty", path, callback=handleDirectoryData)
    elif cmd["type"] == "copy_file_to_server":
        if not cmd["options"]:
            ErrorWindow("No file path or destination path specified")
            return

        filePath, destPath = cmd["options"].split(";")

        if not filePath:
            ErrorWindow("No file path specified")
            return

        if not os.path.exists(filePath):
            ErrorWindow(f'"{filePath}" file not found')
            return

        def handleCopyFileStatus(status: str):
            if status == "OK":
                resMessage = f'"{filePath}" file copied to server'
            else:
                resMessage = f'Cannot copy "{filePath}" file to server'

            sendMessage(
                service,
                reqMessage,
                resMessage,
            )

        sio.emit(
            "DIRECTORY:copyto",
            {
                "metadata": f"{filePath}{SEPARATOR}{destPath}",
                "data": open(filePath, "rb").read(),
            },
            callback=handleCopyFileStatus,
        )
    elif cmd["type"] == "copy_file_to_client":
        if not cmd["options"]:
            ErrorWindow("No file path or destination path specified")
            return

        filePath, destPath = cmd["options"].split(";")

        if not filePath:
            ErrorWindow("No file path specified")
            return

        if not os.path.exists(filePath):
            ErrorWindow(f'"{filePath}" file not found')
            return

        def handleReceiveFileData(data: dict):
            if isinstance(data, dict) and "msg" in data:
                sendMessage(service, reqMessage, data["msg"])
                return

            try:
                fileName = data["filename"]
                fileData = data["fileData"]

                with open(os.path.abspath(destPath) + fileName, "wb") as f:
                    f.write(fileData)
            except Exception:
                sendMessage(
                    service,
                    reqMessage,
                    f'Cannot write "{filePath}" file to client',
                )
                return

        sio.emit("DIRECTORY:copy", filePath, callback=handleReceiveFileData)

    elif cmd["type"] == "delete_file":
        if not cmd["options"]:
            ErrorWindow("No file path specified")
            return

        path = cmd["options"]

        def handleDeleteFileStatus(status: str):
            if "OK":
                resMessage = f'"{path}" file deleted'
            else:
                resMessage = f'Cannot delete "{path}" file'

            sendMessage(
                service,
                reqMessage,
                resMessage,
            )

        sio.emit("DIRECTORY:delete", path, callback=handleDeleteFileStatus)

    elif cmd["type"] == "list_process":

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
                )
            except Exception as e:
                print(e)
            finally:
                os.remove(tmpTextFile)

        sio.emit("APP_PRO:list", "", callback=handleProcessData)
    elif cmd["type"] == "list_application":

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
                )
            except Exception as e:
                print(e)
            finally:
                os.remove(tmpTextFile)

        sio.emit("APP_PRO:list:app", "", callback=handleAppData)

    elif cmd["type"] == "kill_process":
        if not cmd["options"]:
            ErrorWindow("No PID specified")
            return

        pid = cmd["options"]

        def handleKillStatus(status: bool):
            if status:
                sendMessage(
                    service,
                    reqMessage,
                    f"Process with PID {pid} killed",
                )
            else:
                sendMessage(
                    service,
                    reqMessage,
                    f"Process with PID {pid} not found",
                )

        sio.emit("APP_PRO:kill", pid, callback=handleKillStatus)
    else:
        ErrorWindow("Unknown command")


class IndexPage(BasePage):
    def __init__(self, tag: Union[int, str] = "w_index"):
        super().__init__(tag)
        self.service = build("gmail", "v1", credentials=app.creds)
        self.fetchMaxEntries = 5

        self.getData()

    def fetchMail(
        self,
        maxEntries: int = 5,
    ):
        res = (
            self.service.users()
            .messages()
            .list(userId="me", maxResults=maxEntries)
            .execute()
        )
        messages = res["messages"]

        messagePayloads = []
        for message in messages:
            msg = (
                self.service.users()
                .messages()
                .get(userId="me", id=message["id"], format="raw")
                .execute()
            )
            messagePayloads.append(msg)

        return messagePayloads

    def getData(self):
        self.mails = self.fetchMail(maxEntries=self.fetchMaxEntries)

    def handleRefreshClick(self):
        self.getData()
        self.reload(isPrimary=True)

    def render(self):
        with dpg.window(label="Mail Inbox", tag=self.tag, width=400, height=200):
            dpg.add_text("Inbox")

            with dpg.menu_bar():
                with dpg.menu(label="Actions"):
                    dpg.add_menu_item(
                        label="Refresh", callback=lambda: self.handleRefreshClick()
                    )
                    dpg.add_menu_item(
                        label="Exit", callback=lambda: dpg.stop_dearpygui()
                    )

            for mail in self.mails:
                parsedMail = parseMail(mail)

                parsedCmd = []
                if parsedMail["body"] is not None:
                    parsedCmd = parseCmd(parsedMail["body"])

                with dpg.tree_node(
                    label=f'Subject: {parsedMail["subject"]}', default_open=True
                ):
                    dpg.add_text("From: " + parsedMail["from"])
                    dpg.add_text("To: " + parsedMail["to"])
                    dpg.add_text("Date: " + parsedMail["date"])

                    with dpg.tree_node(label="Commands", default_open=True):
                        for cmd in parsedCmd:

                            def handleCmdClick(sender, app_data, user_data):
                                mail = user_data["mail"]
                                cmd = user_data["cmd"]

                                dpg.configure_item(sender, label="Running...")

                                # NOTE: We don't wait for the command to finish
                                # running
                                executor = ThreadPoolExecutor()
                                future = executor.submit(
                                    runCmd,
                                    self.service,
                                    app.sio,
                                    cmd,
                                    mail,
                                )
                                executor.shutdown(wait=False)

                                future.add_done_callback(
                                    lambda _f: dpg.configure_item(sender, label="Done")
                                )

                            with dpg.group(horizontal=True):
                                dpg.add_text(cmd)
                                dpg.add_button(
                                    label="Run",
                                    callback=handleCmdClick,
                                    # NOTE: A little trick to fix the late
                                    # binding problem
                                    user_data={
                                        "cmd": cmd,
                                        "mail": mail,
                                    },
                                )

                        if not parsedCmd:
                            dpg.add_text("No commands found")

                    with dpg.tree_node(label="Body", default_open=True):
                        with dpg.child_window(
                            height=200, autosize_x=True, horizontal_scrollbar=True
                        ):
                            dpg.add_text(parsedMail["body"])
