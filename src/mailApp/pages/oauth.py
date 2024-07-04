import os
from concurrent.futures import ThreadPoolExecutor
from typing import Union

import dearpygui.dearpygui as dpg
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from src.mailApp.app import app
from src.shared.pages.base import BasePage

TOKEN_PATH = "token.json"

CREDENTIALS_PATH = "credentials.json"

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
]

OAUTH_LOCAL_SERVER_PORT = 8080


class OAuthPage(BasePage):
    def __init__(self, tag: Union[int, str] = "w_oauth"):
        super().__init__(tag)

    def handleOAuth(self, parent: Union[int, str]):
        # NOTE: This function doesn't read "redirect_uris" property from
        # "credentials.json" file but "redirect_uri", so we have to
        # explicitly pass it if you don't call "flow.run_local_server()"
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_PATH,
            SCOPES,
            redirect_uri=f"http://localhost:{OAUTH_LOCAL_SERVER_PORT}",
        )

        creds = flow.run_local_server(port=OAUTH_LOCAL_SERVER_PORT)

        return creds

    def render(self):
        with dpg.window(
            label="OAuth",
            tag=self.tag,
            width=400,
            height=200,
            horizontal_scrollbar=True,
        ):
            dpg.add_text("Checking authorization...", tag="t_oauth_status")
            dpg.add_button(
                label="Redirect",
                callback=lambda: app.goto("/"),
                tag="b_redirect",
                show=False,
            )

            if not os.path.exists(CREDENTIALS_PATH):
                dpg.set_value(
                    "t_oauth_status",
                    (
                        "Credentials file not found. Please add it to the root"
                        " directory of application."
                    ),
                )
                return

            # The file token.json stores the user's access and refresh tokens, and
            # is created automatically when the authorization flow completes for the
            # first time.
            if os.path.exists(TOKEN_PATH):
                app.creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

            # If there are no (valid) credentials available, let the user log in.
            if not app.creds or not app.creds.valid:
                if app.creds and app.creds.expired and app.creds.refresh_token:
                    print("Refreshing access token...")
                    dpg.set_value("t_oauth_status", "Refreshing access token...")

                    app.creds.refresh(Request())

                    # Save the credentials for the next run
                    with open(TOKEN_PATH, "w") as token:
                        token.write(app.creds.to_json())

                    dpg.set_value("t_oauth_status", "Authorized")
                    dpg.show_item("b_redirect")

                with ThreadPoolExecutor(max_workers=1) as executor:
                    # REVIEW: Exception can't be caught here, so we have to
                    # find a way to handle it.
                    # NOTE: As the function is defined in the this context, we
                    # don't have to pass other arguments.
                    future = executor.submit(self.handleOAuth, self.tag)
                    creds = future.result()

                    app.creds = creds

                    try:
                        with open(TOKEN_PATH, "w") as token:
                            token.write(creds.to_json())
                    except FileNotFoundError:
                        print("Token file not found")

                    dpg.set_value("t_oauth_status", "Authorized")
                    dpg.configure_item("b_redirect", show=True)

            else:
                dpg.set_value("t_oauth_status", "Authorized")
                dpg.show_item("b_redirect")
