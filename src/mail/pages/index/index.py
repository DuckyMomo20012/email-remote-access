from concurrent.futures import ThreadPoolExecutor
from typing import Union

import dearpygui.dearpygui as dpg
from googleapiclient.discovery import build

from src.mail.app import app
from src.mail.pages.base import BasePage
from src.mail.pages.error import ErrorWindow
from src.shared.mail_processing.index import runCmd
from src.shared.mail_processing.utils import Command, parseCmd
from src.utils.mail import parseMail


def handleRunCmd(service, sio, cmd: Command, reqMessage, reply=True):
    result = runCmd(service, sio, cmd, reqMessage, reply=reply)
    if not result:
        ErrorWindow(
            f"Command {cmd['type']} is not a valid command",
        )


class IndexPage(BasePage):
    def __init__(self, tag: Union[int, str] = "w_index"):
        super().__init__(tag)
        self.service = build("gmail", "v1", credentials=app.creds)
        self.fetchMaxEntries = 5
        self.sendAsReply = True

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
            with dpg.group(horizontal=True):
                dpg.add_text("Inbox")

                def handleFetchMaxEntriesClick(sender, app_data, user_data):
                    self.fetchMaxEntries = int(app_data)
                    self.handleRefreshClick()

                dpg.add_combo(
                    ("5", "10", "15", "20"),
                    default_value=f"{self.fetchMaxEntries}",
                    label="Last mails",
                    width=100,
                    callback=handleFetchMaxEntriesClick,
                )

            with dpg.menu_bar():
                with dpg.menu(label="Actions"):
                    dpg.add_menu_item(
                        label="Refresh", callback=lambda: self.handleRefreshClick()
                    )
                    dpg.add_menu_item(
                        label="Exit", callback=lambda: dpg.stop_dearpygui()
                    )

                def handleSendAsReplyClick(sender, app_data, user_data):
                    print("app_data", app_data)
                    self.sendAsReply = not bool(app_data)

                with dpg.menu(label="Settings"):
                    dpg.add_menu_item(
                        label="Send response as reply",
                        check=True,
                        default_value=self.sendAsReply,
                        callback=handleSendAsReplyClick,
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
                                    handleRunCmd,
                                    self.service,
                                    app.sio,
                                    cmd,
                                    mail,
                                    self.sendAsReply,
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
