# REVIEW: This is a bit messy, we should refactor this later
from src.shared.mail_processing.app_process import (
    onKillProcessMessage,
    onListApplicationMessage,
    onListProcessMessage,
)
from src.shared.mail_processing.directory_tree import (
    onCopyFileToClientMessage,
    onCopyFileToServerMessage,
    onDeleteFileMessage,
    onListDirectoryMessage,
)
from src.shared.mail_processing.live_screen import onScreenshotMessage
from src.shared.mail_processing.mac_address import onMacAddressMessage
from src.shared.mail_processing.shutdown_logout import (
    onLogoutMessage,
    onShutdownMessage,
)
from src.shared.mail_processing.utils import Command

cmdMapping = {
    "shutdown": onShutdownMessage,
    "logout": onLogoutMessage,
    "mac_address": onMacAddressMessage,
    "screenshot": onScreenshotMessage,
    "list_directory": onListDirectoryMessage,
    "copy_file_to_server": onCopyFileToServerMessage,
    "copy_file_to_client": onCopyFileToClientMessage,
    "delete_file": onDeleteFileMessage,
    "list_process": onListProcessMessage,
    "list_application": onListApplicationMessage,
    "kill_process": onKillProcessMessage,
}


def runCmd(service, sio, cmd: Command, reqMessage, reply=True):
    try:
        if cmd["type"] in cmdMapping:
            cmdHandler = cmdMapping[cmd["type"]]
            cmdHandler(service, sio, cmd, reqMessage, reply)
        else:
            return False

        return True
    except Exception as e:
        print(e)
        return False
