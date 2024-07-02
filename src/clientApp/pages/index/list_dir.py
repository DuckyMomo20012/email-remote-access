import os
import re
from typing import Literal, Union

import dearpygui.dearpygui as dpg

from src.clientApp.app import app
from src.server.directory_tree_server import SEPARATOR
from src.shared.pages.base import BasePage
from src.shared.pages.popup import PopupWindow


class ListDirWindow(BasePage):
    def __init__(self, parent: Union[int, str], tag: Union[int, str] = "w_list_dir"):
        super().__init__(tag)
        self.parent = parent
        self.disks: list = []
        self.handler = ""
        self.selectedPath: dict[str, str | bool | None] = {"path": None, "isDir": None}

        self.fetchDisk()

    def refresh(self):
        self.fetchDisk()
        self.reload(isPrimary=False)

    def fetchDisk(self):
        def handleDiskMessage(data: list):
            self.disks = data
            self.reload(isPrimary=False)

        app.sio.emit("DIRECTORY:show_tree", "", callback=handleDiskMessage)

    def fetchDir(self, path, parent):
        def handleDirMessage(data: list | dict):
            if isinstance(data, dict) and "msg" in data:
                msg = " (Access denied)"
                label = dpg.get_item_label(parent)
                if label is not None:
                    dpg.set_item_label(
                        parent,
                        # NOTE: Removes the previous message and adds the new message
                        f"{label.removesuffix(msg)}{msg}",
                    )
                return

            for dir, isDir in data:
                node = dpg.add_tree_node(
                    label=dir,
                    open_on_arrow=True,
                    user_data={"parent": path, "child": dir, "isDir": isDir},
                    parent=parent,
                    leaf=not isDir,
                )

                dpg.bind_item_handler_registry(node, "h_tree_node")

        app.sio.emit("DIRECTORY:list_dirs", path, callback=handleDirMessage)

    def handleTreeNodeClick(self, sender, app_data):
        # NOTE: Can't get user_data directly
        # Ref: https://github.com/hoffstadt/DearPyGui/issues/2283#issuecomment-1940469235
        user_data = dpg.get_item_user_data(app_data[1])
        if not user_data:
            return

        isOpened = dpg.is_item_toggled_open(app_data[1])
        if not isOpened:
            # NOTE: Delete all children nodes, to prevent data duplication
            dpg.delete_item(app_data[1], children_only=True)

        newPath = os.path.join(user_data["parent"], user_data["child"])

        # NOTE: Prevent data duplication
        if user_data["isDir"] and isOpened:
            self.fetchDir(
                path=newPath,
                parent=app_data[1],
            )

        dpg.set_value("t_path", newPath)

        self.selectedPath = {
            "path": newPath,
            "isDir": user_data["isDir"],
        }

    def handleSendFile(self, app_data, selectedPath):
        for fileName in app_data["selections"]:
            filePath = app_data["selections"][fileName]
            # NOTE: Add trailing slash to destPath
            destPath = os.path.join(selectedPath["path"], "")

            # NOTE: Force early binding to avoid late binding error
            # Ref: https://stackoverflow.com/questions/3431676/creating-functions-or-lambdas-in-a-loop-or-comprehension
            def handleMessage(status: Literal["OK", "NOT OK"], fileName=fileName):
                if status == "OK":
                    PopupWindow(f"Copy file {fileName} successfully!", label="Success!")

                else:
                    PopupWindow(f"Cannot copy file {fileName}!", label="Error!")

            app.sio.emit(
                "DIRECTORY:copyto",
                {
                    "metadata": f"{filePath}{SEPARATOR}{destPath}",
                    "data": open(filePath, "rb").read(),  # noqa: SIM115
                },
                # NOTE: We don't need to pass fileName as a parameter to the
                # callback function because we are binding it to the function itself
                callback=handleMessage,
            )

    def handleSendFileClick(self):
        if not self.selectedPath["isDir"]:
            PopupWindow("Please select a folder", label="Error!")
            return

        dialog = dpg.add_file_dialog(
            height=350,
            callback=lambda sender, app_data: self.handleSendFile(
                app_data, self.selectedPath
            ),
            cancel_callback=lambda: dpg.delete_item(dialog),
        )
        dpg.add_file_extension(".*", parent=dialog)

    def handleReceiveFile(self, app_data, selectedPath):
        for dir in app_data["selections"]:
            filePath = selectedPath["path"]
            # NOTE: Add trailing slash to destPath
            # NOTE: Somehow the last dir is duplicated
            destDir = os.path.join(app_data["selections"][dir].removesuffix(dir), "")
            # NOTE: Remove the number of files selected
            destDir = re.sub(r"(\d+ files Selected){1}.+$", "", destDir)

            # NOTE: Force early binding to avoid late binding error
            # Ref: https://stackoverflow.com/questions/3431676/creating-functions-or-lambdas-in-a-loop-or-comprehension
            def handleMessage(data: dict, filePath=filePath, destDir=destDir):
                if isinstance(data, dict) and "msg" in data:
                    PopupWindow(f"Cannot receive {filePath}", label="Error!")
                    return

                with open(os.path.join(destDir, data["filename"]), "wb") as f:
                    f.write(data["fileData"])

                PopupWindow(f"Copy {filePath} successfully!", label="Success!")

            app.sio.emit(
                "DIRECTORY:copy",
                filePath,
                callback=handleMessage,
            )

    def handleReceiveFileClick(self):
        if self.selectedPath["isDir"]:
            PopupWindow("Please select a file", label="Error!")
            return

        dialog = dpg.add_file_dialog(
            directory_selector=True,
            height=350,
            callback=lambda sender, app_data: self.handleReceiveFile(
                app_data, self.selectedPath
            ),
            cancel_callback=lambda: dpg.delete_item(dialog),
        )

    def handleDeleteFileClick(self):
        if self.selectedPath["isDir"]:
            PopupWindow("Please select a file", label="Error!")
            return

        filePath = self.selectedPath["path"]

        def handleMessage(status: Literal["OK", "NOT OK"], filePath):
            if status == "OK":
                PopupWindow(f"Delete {filePath} successfully!", label="Success!")
            else:
                PopupWindow(f"Cannot delete {filePath}!", label="Error!")

        app.sio.emit(
            "DIRECTORY:delete",
            filePath,
            callback=lambda status: handleMessage(status, filePath),
        )

    def render(self):
        if dpg.does_item_exist("h_tree_node"):
            dpg.delete_item("h_tree_node")

        with dpg.item_handler_registry(tag="h_tree_node"):
            dpg.add_item_clicked_handler(callback=self.handleTreeNodeClick)

        with dpg.group(tag=self.tag, parent=self.parent):  # noqa: SIM117
            with dpg.group(horizontal=True):
                dpg.add_button(label="Refresh", callback=self.refresh)

            with dpg.group(horizontal=True):
                dpg.add_input_text(readonly=True, tag="t_path", width=250)

                with dpg.group(horizontal=True):
                    receiveBtn = dpg.add_button(
                        label="Send",
                        tag="b_send_file",
                        callback=self.handleSendFileClick,
                    )
                    with dpg.tooltip(receiveBtn):
                        dpg.add_text("Send file to destination folder on server")

                    sendBtn = dpg.add_button(
                        label="Receive",
                        tag="b_receive_file",
                        callback=self.handleReceiveFileClick,
                    )
                    with dpg.tooltip(sendBtn):
                        dpg.add_text("Receive file from server")

                    deleteBtn = dpg.add_button(
                        label="Delete",
                        tag="b_delete_file",
                        callback=self.handleDeleteFileClick,
                    )
                    with dpg.tooltip(deleteBtn):
                        dpg.add_text("Delete file")

            with dpg.child_window():
                for disk in self.disks:
                    node = dpg.add_tree_node(
                        # NOTE: Please ensure disk user_data matches dir user_data
                        label=disk,
                        open_on_arrow=True,
                        user_data={"parent": disk, "child": "", "isDir": True},
                    )
                    dpg.bind_item_handler_registry(node, "h_tree_node")
