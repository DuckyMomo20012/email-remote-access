import os
import webbrowser
from multiprocessing.pool import ThreadPool
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
    def __init__(self, redirect: BasePage, tag: Union[int, str] = "w_oauth"):
        super().__init__(tag)
        self.redirect = redirect

    def render(self):
        dpg.add_window(
            label="OAuth",
            tag=self.tag,
            width=400,
            height=200,
            horizontal_scrollbar=True,
        )
        dpg.add_text("Checking authorization...", parent=self.tag, tag="t_oauth_status")
        dpg.add_button(
            label="Redirect",
            callback=lambda: app.goto(self.redirect()),
            parent=self.tag,
            tag="b_redirect",
            show=False,
        )

        # The file token.json stores the user's access and refresh tokens, and
        # is created automatically when the authorization flow completes for the
        # first time.
        if os.path.exists(TOKEN_PATH):
            app.creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not app.creds or not app.creds.valid:
            if app.creds and app.creds.expired and app.creds.refresh_token:
                dpg.set_value("t_oauth_status", "Refreshing access token...")

                app.creds.refresh(Request())

                # Save the credentials for the next run
                with open(TOKEN_PATH, "w") as token:
                    token.write(app.creds.to_json())

                dpg.set_value("t_oauth_status", "Authorized")
                dpg.configure_item("b_redirect", show=True)
            else:
                # NOTE: run_local_server() is blocking, so we have to run it in
                # a thread.
                def handleThread():
                    # NOTE: This function doesn't read "redirect_uris" property from
                    # "credentials.json" file but "redirect_uri", so we have to
                    # explicitly pass it if you don't call "flow.run_local_server()"
                    flow = InstalledAppFlow.from_client_secrets_file(
                        CREDENTIALS_PATH,
                        SCOPES,
                        redirect_uri=f"http://localhost:{OAUTH_LOCAL_SERVER_PORT}",
                    )

                    dpg.set_value(
                        "t_oauth_status",
                        (
                            "Please continue the authorization in the opened "
                            "browser window, or visit the following URL:"
                        ),
                    )
                    auth_url, _ = flow.authorization_url()

                    dpg.add_button(
                        tag="b_auth_url",
                        label=f"{auth_url}",
                        callback=lambda: webbrowser.open(auth_url),
                        parent=self.tag,
                    )

                    app.creds = flow.run_local_server(port=OAUTH_LOCAL_SERVER_PORT)

                    # Save the credentials for the next run
                    with open(TOKEN_PATH, "w") as token:
                        token.write(app.creds.to_json())

                    dpg.set_value("t_oauth_status", "Authorized")
                    dpg.configure_item("b_redirect", show=True)

                with ThreadPool(processes=1) as pool:
                    # REVIEW: Exception can't be caught here, so we have to
                    # find a way to handle it.
                    # NOTE: As the function is defined in the this context, we
                    # don't have to pass other arguments.
                    pool.apply_async(handleThread)

        else:
            dpg.set_value("t_oauth_status", "Authorized")
            dpg.configure_item("b_redirect", show=True)
