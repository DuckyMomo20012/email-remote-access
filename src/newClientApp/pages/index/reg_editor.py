import json
from typing import Union

import dearpygui.dearpygui as dpg

from src.newClientApp.app import app
from src.shared.pages.base import BasePage
from src.shared.pages.popup import PopupWindow

actionMap = {
    "get_value": 1,
    "set_value": 2,
    "create_key": 3,
    "delete_key": 4,
}


class RegistryEditorWindow(BasePage):
    def __init__(self, parent: Union[int, str], tag: Union[int, str] = "w_reg_editor"):
        super().__init__(tag)
        self.parent = parent
        self.action = ""
        self.keyVal = ""
        self.nameVal = ""
        self.dataVal = ""
        self.dataTypeVal = ""

    def handleActionClick(self, sender, app_data, user_data):
        self.action = user_data

        actionLabel = dpg.get_item_label(sender)
        dpg.set_value("t_action", f"Current action: {actionLabel}")

        if user_data == "create_key" or user_data == "delete_key":
            dpg.configure_item("key_val", enabled=True)
            dpg.configure_item("name_val", enabled=False)
            dpg.configure_item("data_val", enabled=False)
            dpg.configure_item("data_type_val", enabled=False)
            dpg.configure_item("b_submit", enabled=True)

            dpg.set_value("name_val", "")
            dpg.set_value("data_val", "")
            dpg.set_value("data_type_val", "")

        elif user_data == "get_value":
            dpg.configure_item("key_val", enabled=True)
            dpg.configure_item("name_val", enabled=True)
            dpg.configure_item("data_val", enabled=False)
            dpg.configure_item("data_type_val", enabled=False)
            dpg.configure_item("b_submit", enabled=True)

            dpg.set_value("name_val", self.nameVal)
            dpg.set_value("data_val", "")
            dpg.set_value("data_type_val", "")

        elif user_data == "set_value":
            dpg.configure_item("key_val", enabled=True)
            dpg.configure_item("name_val", enabled=True)
            dpg.configure_item("data_val", enabled=True)
            dpg.configure_item("data_type_val", enabled=True)
            dpg.configure_item("b_submit", enabled=True)

            # NOTE: Restore previous value
            dpg.set_value("name_val", self.nameVal)
            dpg.set_value("data_val", self.dataVal)
            dpg.set_value("data_type_val", self.dataTypeVal)

    def handleSubmitClick(self):
        actionId = actionMap[self.action]
        # NOTE: Closure to get the current value of the input
        keyVal = self.keyVal
        nameVal = self.nameVal
        dataVal = self.dataVal
        dataTypeVal = self.dataTypeVal

        msg = {
            "ID": actionId,
            "path": keyVal,
            "name_value": nameVal,
            "value": dataVal,
            "v_type": dataTypeVal,
        }
        msg = json.dumps(msg)
        msg_bytes = bytes(msg, "utf8")

        def handleMessage(data: tuple[str, str]):
            [res1, res2] = data

            if res1 == "0":
                PopupWindow("Something wrong happened", "Error")
                return

            if actionId == 1 and res2 != "0":
                PopupWindow(
                    f"Value {nameVal} is: " + str(res2), "Success", autoClose=False
                )
            elif actionId == 2:
                PopupWindow(f"Set value for {nameVal} successfully", "Success")
            elif actionId == 3:
                PopupWindow(f"Create key {keyVal} successfully", "Success")
            elif actionId == 4:
                PopupWindow(f"Delete key {keyVal} successfully", "Success")

        app.sio.emit("REGISTRY:edit", msg_bytes, callback=handleMessage)

    def handleDataTypeClick(self, sender, app_data, user_data):
        self.dataTypeVal = app_data

        if app_data == "REG_MULTI_SZ":
            dpg.configure_item("data_val", multiline=True, height=100)
        else:
            if "\n" in self.dataVal:
                # NOTE: Replace newline with space
                self.dataVal = self.dataVal.replace("\n", " ")
                dpg.set_value("data_val", self.dataVal)

            dpg.configure_item("data_val", multiline=False, height=0)

    def render(self):
        with dpg.group(tag=self.tag, parent=self.parent):  # noqa: SIM117
            dpg.add_text("Choose an action to continue:")
            with dpg.group(horizontal=True):
                dpg.add_button(
                    tag="b_create_key",
                    label="Create key",
                    user_data="create_key",
                    callback=self.handleActionClick,
                )
                dpg.add_button(
                    tag="b_delete_key",
                    label="Delete key",
                    user_data="delete_key",
                    callback=self.handleActionClick,
                )
                dpg.add_button(
                    tag="b_get_value",
                    label="Get value",
                    user_data="get_value",
                    callback=self.handleActionClick,
                )
                dpg.add_button(
                    tag="b_set_value",
                    label="Set value",
                    user_data="set_value",
                    callback=self.handleActionClick,
                )

            dpg.add_text("Current action: None", tag="t_action")

            with dpg.child_window(height=-100):
                dpg.add_input_text(
                    label="Key",
                    tag="key_val",
                    enabled=False,
                    callback=lambda sender, app_data: self.__setattr__(
                        "keyVal", app_data
                    ),
                )
                dpg.add_input_text(
                    label="Name",
                    tag="name_val",
                    enabled=False,
                    callback=lambda sender, app_data: self.__setattr__(
                        "nameVal", app_data
                    ),
                )
                dpg.add_input_text(
                    label="Data",
                    tag="data_val",
                    enabled=False,
                    callback=lambda sender, app_data: self.__setattr__(
                        "dataVal", app_data
                    ),
                )

                dpg.add_combo(
                    [
                        "REG_SZ",
                        "REG_BINARY",
                        "REG_DWORD",
                        "REG_QWORD",
                        "REG_MULTI_SZ",
                        "REG_EXPAND_SZ",
                    ],
                    label="Data type",
                    tag="data_type_val",
                    enabled=False,
                    callback=self.handleDataTypeClick,
                )

            dpg.add_button(
                tag="b_submit",
                label="Submit",
                enabled=False,
                callback=self.handleSubmitClick,
            )
