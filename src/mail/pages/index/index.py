import base64
import email
import re
from concurrent.futures import ThreadPoolExecutor
from typing import Literal, Optional, TypedDict, Union, cast

import dearpygui.dearpygui as dpg
from googleapiclient.discovery import build

from src.mail.app import app
from src.mail.pages.base import BasePage
from src.utils.mail import composeMail, parseMail


class Command(TypedDict):
    type: Literal[
        "shutdown",
        "logout",
        "mac_address",
        "screenshot",
        "list_directory",
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
    "list_process",
    "list_application",
    "kill_process",
]


def parseMessage(msg):
    cmd = []

    parsedMsg = parseMail(msg)

    if parsedMsg["body"] is not None:
        cmd = parseCmd(parsedMsg["body"])

    return {
        **parsedMsg,
        "cmd": cmd,
    }


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
        mails = self.fetchMail(maxEntries=self.fetchMaxEntries)
        self.mails = [parseMessage(mail) for mail in mails]

    def runCmd(self, cmd: Command, toUser: str):
        # TODO: Switch each command and send desired command to "toUser"
        # NOTE: Use "self.service" to send email
        # NOTE: Use "app.sio" to register socket.io event callback (emit
        # events/listen for response)

        # This will send a "foo" event to the server with "some_data" as the
        # data and receive a response from the server. It's like req/res in a
        # web server.
        # E.g.:
        # app.sio.emit("foo", "some_data", callback=lambda data: print(data))

        # This will send a "foo" event to the server with "some_data" as the
        # data and listen for a "bar" event from the server. It's quite like the
        # above approach but it's more like a pub/sub model.
        # E.g.:
        # app.sio.emit("foo", "some_data")

        # @app.sio.on("bar")
        # def on_bar(data):
        #     pass

        pass

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
                with dpg.tree_node(
                    label=f'Subject: {mail["subject"]}', default_open=True
                ):
                    dpg.add_text("From: " + mail["from"])
                    dpg.add_text("To: " + mail["to"])
                    dpg.add_text("Date: " + mail["date"])

                    with dpg.tree_node(label="Commands", default_open=True):
                        for cmd in mail["cmd"]:

                            def handleCmdClick(sender, app_data, user_data):
                                parsedMsg = user_data["parsedMsg"]
                                cmd = user_data["cmd"]

                                dpg.configure_item(sender, label="Running...")

                                # NOTE: We don't wait for the command to finish
                                # running
                                executor = ThreadPoolExecutor()
                                future = executor.submit(
                                    self.runCmd,
                                    self.service,
                                    app.sio,
                                    cmd,
                                    mail["from"],
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
                                        "parsedMsg": mail,
                                    },
                                )

                        if not mail["cmd"]:
                            dpg.add_text("No commands found")

                    with dpg.tree_node(label="Body", default_open=True):
                        with dpg.child_window(
                            height=200, autosize_x=True, horizontal_scrollbar=True
                        ):
                            dpg.add_text(mail["body"])
