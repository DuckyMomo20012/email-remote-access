from typing import Literal, Union

import dearpygui.dearpygui as dpg

from src.clientApp.app import app
from src.shared.pages.base import BasePage
from src.shared.pages.confirm import ConfirmWindow
from src.shared.pages.popup import PopupWindow


class ListProcessWindow(BasePage):
    def __init__(self, parent: Union[int, str], tag: Union[int, str] = "w_list_proc"):
        super().__init__(tag)
        self.parent = parent
        self.filter: dict[str, bool] = {"app": True, "proc": True}
        self.filterFlag: Literal["Process", "Application"] = "Process"
        self.data: list[dict] = []
        self.selected_proc: set[str] = set()

        self.fetchProcess()

    def refresh(self):
        self.fetchProcess()
        self.reload(isPrimary=False)

    def fetchProcess(self):
        def handleMessageWrapper(data: list[dict], err, type):
            def handleMessage(data: list[dict], err):
                if err is not None:
                    PopupWindow(err["message"], label="Error!")
                    return

                self.data = []
                for proc in data:
                    self.data = [
                        *self.data,
                        {
                            "name": proc["name"],
                            "pid": proc["id"],
                            "threadCount": proc["threads"],
                            "cpuPercent": round(proc["cpu_percent"], 2),
                            "memoryPercent": round(proc["memory_percent"], 2),
                            "type": type,
                        },
                    ]
                self.reload(isPrimary=False)

            return handleMessage(data, err)

        if self.filter["proc"] is True:
            app.sio.emit(
                "APP_PRO:list",
                "",
                callback=lambda data, err: handleMessageWrapper(data, err, "proc"),
            )
        elif self.filter["app"] is True:
            app.sio.emit(
                "APP_PRO:list:app",
                "",
                callback=lambda data, err: handleMessageWrapper(data, err, "app"),
            )

    def handleRowClick(self, sender, app_data, user_data):
        if app_data is True:
            # NOTE: We add the pid passed by "user_data"
            self.selected_proc.add(user_data)
        else:
            self.selected_proc.remove(user_data)

        self.reload(isPrimary=False)

    def handleRemove(self, pid):
        self.selected_proc.remove(pid)
        # NOTE: Refresh to update data
        self.refresh()

    def handleKillOne(self, pid):
        def handleMessage(data, err):
            if err is not None:
                PopupWindow(
                    f"Cannot kill process {data}: {err["message"]}", label="Error!"
                )
            else:
                self.handleRemove(data)

                PopupWindow(f"Process {data} killed", label="Success!")

        app.sio.emit("APP_PRO:kill", pid, callback=handleMessage)

    def handleKillAll(self):
        for id in self.selected_proc:
            self.handleKillOne(id)

    def handleFilter(self, sender, app_data, user_data):
        if app_data == "All":
            self.filter["app"] = True
            self.filter["proc"] = True
        elif app_data == "Process":
            self.filter["app"] = False
            self.filter["proc"] = True
        elif app_data == "Application":
            self.filter["app"] = True
            self.filter["proc"] = False

        self.filterFlag = app_data
        self.refresh()

    def render(self):
        with dpg.group(tag=self.tag, parent=self.parent):
            with dpg.group(horizontal=True):
                dpg.add_button(label="Refresh", callback=self.refresh)

                dpg.add_combo(
                    ["Process", "Application"],
                    label="Filter",
                    default_value=self.filterFlag,
                    callback=self.handleFilter,
                )

            n_selected = len(self.selected_proc)
            if n_selected:
                with dpg.group(horizontal=True):
                    dpg.add_text(f"{n_selected} id(s) selected")

                    dpg.add_button(
                        label="Kill all selected",
                        callback=lambda: ConfirmWindow(
                            "Do you want to kill this process?",
                            handleConfirm=self.handleKillAll,
                        ),
                    )

                with dpg.child_window(height=150):
                    for pid in self.selected_proc:
                        proc = next((p for p in self.data if p["pid"] == pid), None)

                        if proc is None:
                            continue

                        if self.filter[proc["type"]] is False:
                            continue

                        with dpg.group(horizontal=True):
                            dpg.add_text(f"{pid}:{proc["name"]}")
                            dpg.add_button(
                                label="Remove",
                                user_data=pid,
                                callback=lambda sender,
                                app_data,
                                user_data: self.handleRemove(user_data),
                            )
                            dpg.add_button(
                                label="Kill",
                                user_data=pid,
                                callback=lambda sender,
                                app_data,
                                user_data: ConfirmWindow(
                                    "Do you want to kill this process?",
                                    handleConfirm=lambda: self.handleKillOne(user_data),
                                ),
                            )

            with dpg.child_window():  # noqa: SIM117
                with dpg.table(header_row=True, resizable=True):
                    dpg.add_table_column(label="Process Id")
                    dpg.add_table_column(label="Process Name")
                    dpg.add_table_column(label="Thread Count")
                    dpg.add_table_column(label="CPU Percent")
                    dpg.add_table_column(label="Memory Percent")

                    for data in self.data:
                        with dpg.table_row():
                            # NOTE: We don't have to set "callback" multiple
                            # times, because of "span_columns"
                            dpg.add_selectable(
                                label=data["pid"],
                                user_data=data["pid"],
                                span_columns=True,
                                default_value=data["pid"] in self.selected_proc,
                                callback=self.handleRowClick,
                            )
                            dpg.add_selectable(label=data["name"])
                            dpg.add_selectable(label=data["threadCount"])
                            dpg.add_selectable(label=data["cpuPercent"])
                            dpg.add_selectable(label=data["memoryPercent"])
