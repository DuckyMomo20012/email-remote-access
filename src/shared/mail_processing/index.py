# REVIEW: This is a bit messy, we should refactor this later
import socketio

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
from src.shared.mail_processing.registry import (
    onCreateRegKey,
    onDeleteRegKey,
    onGetRegValue,
    onSetRegValue,
)
from src.shared.mail_processing.shutdown_logout import (
    onLogoutMessage,
    onShutdownMessage,
)
from src.shared.mail_processing.sys_info import onSysInfoMessage
from src.shared.mail_processing.utils import Command

cmdMapping = {
    "shutdown": onShutdownMessage,
    "logout": onLogoutMessage,
    "sys_info": onSysInfoMessage,
    "screenshot": onScreenshotMessage,
    "list_directory": onListDirectoryMessage,
    "copy_file_to_server": onCopyFileToServerMessage,
    "copy_file_to_client": onCopyFileToClientMessage,
    "delete_file": onDeleteFileMessage,
    "list_process": onListProcessMessage,
    "list_application": onListApplicationMessage,
    "kill_process": onKillProcessMessage,
    "create_registry_key": onCreateRegKey,
    "delete_registry_key": onDeleteRegKey,
    "get_registry_value": onGetRegValue,
    "set_registry_value": onSetRegValue,
}


def runCmd(service, sio: socketio.Client, cmd: Command, reqMessage, reply=True):
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
