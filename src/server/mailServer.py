import os

import socketio
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from socketio.exceptions import ConnectionError

from src.server.server import PORT
from src.shared.mail_processing.index import runCmd
from src.shared.mail_processing.utils import parseCmd
from src.utils.mail import parseMail

TOKEN_PATH = "token.json"

CREDENTIALS_PATH = "credentials.json"

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
]

OAUTH_LOCAL_SERVER_PORT = 8081

LOG_FILE = "tmp/log.txt"

DELAY_BETWEEN_RUNS = 2

DEFAULT_BOX = "INBOX"


class MailClient:
    sio: socketio.Client

    def __init__(self, serverHost: str = "localhost", serverPort: int = PORT):
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.fetchInterval = 5
        self.fetchMaxEntries = 5
        self.creds = None
        self.sio = socketio.Client()

        self.authorize()

        self.service = build("gmail", "v1", credentials=self.creds)

        self.connect()

    def __del__(self):
        self.sio.disconnect()

    def connect(self):
        # NOTE:
        self.sio.connect(f"http://{self.serverHost}:{self.serverPort}")
        try:
            pass
        except ConnectionError:
            print("Connection error")

    def authorize(self):
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(TOKEN_PATH):
            self.creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH,
                    SCOPES,
                    redirect_uri=f"http://localhost:{OAUTH_LOCAL_SERVER_PORT}",
                )
                self.creds = flow.run_local_server(port=OAUTH_LOCAL_SERVER_PORT)
            # Save the credentials for the next run
            with open(TOKEN_PATH, "w") as token:
                token.write(self.creds.to_json())

    def fetchMail(
        self,
        maxEntries: int = 5,
    ):
        res = (
            self.service.users()
            .messages()
            .list(userId="me", maxResults=maxEntries, labelIds=[DEFAULT_BOX])
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

    def processMail(self):
        while True:
            mails = self.fetchMail(maxEntries=self.fetchMaxEntries)

            for mail in mails:
                parsedMail = parseMail(mail)

                date = parsedMail["date"]

                if os.path.exists(LOG_FILE):
                    with open(LOG_FILE, "r") as f:
                        if date in f.read():
                            continue
                else:
                    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
                    open(LOG_FILE, "w")

                parsedCmd = []
                if parsedMail["body"] is not None:
                    parsedCmd = parseCmd(parsedMail["body"])

                    for cmd in parsedCmd:
                        result = runCmd(self.service, self.sio, cmd, mail)
                        # NOTE: Don't spam the server
                        self.sio.sleep(DELAY_BETWEEN_RUNS)

                        if result:
                            with open(LOG_FILE, "a") as f:
                                f.write(f"{date}: {cmd}\n")
            self.sio.sleep(self.fetchInterval)


def main():
    mailClient = MailClient()
    mailClient.processMail()
