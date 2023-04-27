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


def runCmd(service, sio, cmd: Command, reqMessage, reply=True):
    try:
        if cmd["type"] == "shutdown":
            onShutdownMessage(service, sio, cmd, reqMessage, reply=reply)
        elif cmd["type"] == "logout":
            onLogoutMessage(service, sio, cmd, reqMessage, reply=reply)
        elif cmd["type"] == "mac_address":
            onMacAddressMessage(service, sio, cmd, reqMessage, reply=reply)
        elif cmd["type"] == "screenshot":
            onScreenshotMessage(service, sio, cmd, reqMessage, reply=reply)
        elif cmd["type"] == "list_directory":
            onListDirectoryMessage(service, sio, cmd, reqMessage, reply=reply)
        elif cmd["type"] == "copy_file_to_server":
            onCopyFileToServerMessage(service, sio, cmd, reqMessage, reply=reply)
        elif cmd["type"] == "copy_file_to_client":
            onCopyFileToClientMessage(service, sio, cmd, reqMessage, reply=reply)
        elif cmd["type"] == "delete_file":
            onDeleteFileMessage(service, sio, cmd, reqMessage, reply=reply)
        elif cmd["type"] == "list_process":
            onListProcessMessage(service, sio, cmd, reqMessage, reply=reply)
        elif cmd["type"] == "list_application":
            onListApplicationMessage(service, sio, cmd, reqMessage, reply=reply)
        elif cmd["type"] == "kill_process":
            onKillProcessMessage(service, sio, cmd, reqMessage, reply=reply)
        else:
            return False

        return True
    except Exception as e:
        print(e)
        return False
