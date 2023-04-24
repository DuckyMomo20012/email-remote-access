from typing import Literal, Union

import dearpygui.dearpygui as dpg
from googleapiclient.discovery import build

from src.mail.app import app
from src.mail.pages.base import BasePage
from src.utils.mail import parseMail

Command = Literal[
    "shutdown",
    "logout",
    "mac_address",
    "screenshot",
    "list_directory",
    "list_process",
    "list_application",
    "kill_process",
]

DEFAULT_COMMANDS: list[Command] = [
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
    return [cmd for cmd in DEFAULT_COMMANDS if cmd in msg]


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
                                dpg.configure_item(sender, label="Running...")

                                # Sleep for 5 second to simulate running
                                # time.sleep(5)

                                self.runCmd(cmd, mail["from"])

                                dpg.configure_item(sender, label="Done")

                            with dpg.group(horizontal=True):
                                dpg.add_text(cmd)
                                dpg.add_button(label="Run", callback=handleCmdClick)

                        if not mail["cmd"]:
                            dpg.add_text("No commands found")

                    with dpg.tree_node(label="Body", default_open=True):
                        with dpg.child_window(
                            height=200, autosize_x=True, horizontal_scrollbar=True
                        ):
                            dpg.add_text(mail["body"])
