import base64
import email
import email.header
import email.utils
from typing import Literal, Union

import dearpygui.dearpygui as dpg
from googleapiclient.discovery import build

from src.mail.app import app
from src.mail.pages.base import BasePage

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


def parseMail(msg):
    date = ""
    subject = ""
    fromUser = ""
    toUser = ""
    body = ""
    cmd = []

    parsedMsg = email.message_from_bytes(base64.urlsafe_b64decode(msg["raw"]))

    if parsedMsg["Date"] is not None:
        dateRaw = parsedMsg["Date"]
        parsedDate = email.utils.parsedate_to_datetime(dateRaw)
        date = parsedDate.strftime("%Y-%m-%d %H:%M:%S")

    if parsedMsg["Subject"] is not None:
        subject = email.header.decode_header(parsedMsg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

    if parsedMsg["From"] is not None:
        fromUser = email.header.decode_header(parsedMsg["From"])[0][0]
        if isinstance(fromUser, bytes):
            fromUser = fromUser.decode()

    if parsedMsg["To"] is not None:
        toUser = email.header.decode_header(parsedMsg["To"])[0][0]
        if isinstance(toUser, bytes):
            toUser = toUser.decode()

    body_data = []
    if parsedMsg.is_multipart():
        for part in parsedMsg.get_payload():
            if "text" in part.get_content_maintype():
                body_data.append(part.get_payload(decode=True).decode("utf-8"))
    else:
        body_data = parsedMsg.get_payload(decode=True).decode("utf-8")
    if body_data is not None:
        body = "".join(body_data)

    if body:
        cmd = parseCmd(body)

    return {
        "date": date,
        "subject": subject,
        "from": fromUser,
        "to": toUser,
        "body": body,
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
        self.mails = [parseMail(mail) for mail in mails]

    def runCmd(self, cmd: Command):
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

                                self.runCmd(cmd)

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
