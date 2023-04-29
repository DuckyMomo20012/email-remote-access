import base64
import email
import re
from typing import Literal, Optional, TypedDict, cast

from src.utils.mail import composeMail


class Command(TypedDict):
    type: Literal[
        "shutdown",
        "logout",
        "sys_info",
        "screenshot",
        "list_directory",
        "copy_file_to_server",
        "copy_file_to_client",
        "copy_file_to_client_stream",
        "delete_file",
        "list_process",
        "list_application",
        "kill_process",
        "create_registry_key",
        "delete_registry_key",
        "get_registry_value",
        "set_registry_value",
    ]
    options: Optional[str]
    autoRun: bool


DEFAULT_COMMANDS = [
    "shutdown",
    "logout",
    "sys_info",
    "screenshot",
    "list_directory",
    "copy_file_to_server",
    "copy_file_to_client",
    "copy_file_to_client_stream",
    "delete_file",
    "list_process",
    "list_application",
    "kill_process",
    "create_registry_key",
    "delete_registry_key",
    "get_registry_value",
    "set_registry_value",
]


def parseCmd(msg: str) -> list[Command]:
    # NOTE: The pattern was not intentionally escaped to join the commands with
    # `|`
    cmdPattern = "|".join(DEFAULT_COMMANDS)

    # NOTE: We limit the options to only alphanumeric and `\\`, `:`, `;`, `.` to
    # increase the matching accuracy. The `\\`, `:`, `.` was included in the
    # options for the file path. The `;` was included for splitting options.
    pattern = (
        rf"(?P<autoRun>#|!)?\((?P<type>{cmdPattern})(?:\:(?P<options>[\w\\:;\.]*))?\)"
    )

    result = re.finditer(pattern, msg)

    cmdUnique: list[Command] = []

    for match in result:
        autoRun, type, options = match.group("autoRun", "type", "options")

        if autoRun == "#":
            autoRunVal = True
        elif autoRun == "!":
            autoRunVal = False
        else:
            autoRunVal = False

        newCmd = cast(
            Command,
            {
                "autoRun": autoRunVal,
                "type": type,
                "options": options,
            },
        )

        # NOTE: This is just a simple way to remove duplicate commands from the
        # list
        if newCmd not in cmdUnique:
            cmdUnique.append(newCmd)

    return cmdUnique


# NOTE: This acts as a wrapper as we have to prepare some metadata before
# sending the message
def sendMessage(service, reqMessage, body, attachments=None, reply=True):
    if attachments is None:
        attachments = []
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
