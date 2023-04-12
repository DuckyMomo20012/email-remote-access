import tkinter as tk
from tkinter import messagebox

import socketio

import src.client.app_process_client as ap
import src.client.directory_tree_client as dt
import src.client.entrance_ui as ui1
import src.client.keylogger_client as kl
import src.client.live_screen_client as lsc
import src.client.mac_address_client as mac
import src.client.main_ui as ui2
import src.client.registry_client as rc
import src.client.shutdown_logout_client as sl
from src.server.server import PORT


class ClientApp:
    sio = socketio.Client(logger=True)

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x600")
        self.root.configure(bg="#FFFFFF")
        self.root.title("Client")
        self.root.resizable(False, False)

        self.root.protocol("WM_DELETE_WINDOW", self.__del__)

        self.f1 = ui1.Entrance_UI(self.root)
        self.f1.button_1.configure(command=self.connectServer)

    def __del__(self):
        self.sio.disconnect()

        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def start(self):
        self.root.mainloop()

    def callbacks(self):
        @self.sio.event
        def connect():
            messagebox.showinfo(message="Connect successfully!")

            self.show_main_ui()

        @self.sio.event
        def connect_error(data):
            messagebox.showerror(message="Cannot connect!")

    def back(self, ui):
        ui.place_forget()
        f2.place(x=0, y=0)
        self.sio.emit("QUIT")

    def live_screen(self):
        self.sio.emit("LIVESCREEN:start")
        tmp = lsc.Desktop_UI(self.root, self.sio)
        if not tmp.status:
            self.back(tmp)
        return

    def shutdown_logout(self):
        sl.shutdown_logout(self.sio, self.root)
        return

    def mac_address(self):
        self.sio.emit("MAC:info")
        mac.mac_address(self.sio)
        return

    def back_dirTree(self, ui):
        ui.place_forget()
        ui.tree.pack_forget()
        f2.place(x=0, y=0)
        self.sio.emit("QUIT")

    def directory_tree(self):
        tmp = dt.DirectoryTree_UI(self.root, self.sio)
        tmp.button_6.configure(command=lambda: self.back_dirTree(tmp))
        return

    def app_process(self):
        tmp = ap.App_Process_UI(self.root, self.sio)
        tmp.button_6.configure(command=lambda: self.back(tmp))
        return

    def disconnect(self):
        f2.place_forget()
        self.f1.place(x=0, y=0)
        self.sio.emit("QUIT")
        return

    def keylogger(self):
        self.sio.emit("KEYLOG:start")
        tmp = kl.Keylogger_UI(self.root, self.sio)
        tmp.button_6.configure(command=lambda: self.back(tmp))
        return

    def registry(self):
        tmp = rc.Registry_UI(self.root, self.sio)
        tmp.btn_back.configure(command=lambda: self.back_reg(tmp))
        return

    def back_reg(self, ui):
        self.sio.emit("REGISTRY:stop")
        ui.place_forget()
        f2.place(x=0, y=0)

    def show_main_ui(self):
        self.f1.place_forget()
        global f2
        f2 = ui2.Main_UI(self.root)
        f2.button_1.configure(command=self.live_screen)
        f2.button_2.configure(command=self.registry)
        f2.button_3.configure(command=self.mac_address)
        f2.button_4.configure(command=self.directory_tree)
        f2.button_5.configure(command=self.app_process)
        f2.button_6.configure(command=self.disconnect)
        f2.button_7.configure(command=self.keylogger)
        f2.button_8.configure(command=self.shutdown_logout)
        return

    def connectServer(self):
        # NOTE: Register the callbacks
        self.callbacks()

        ip = self.f1.input.get()

        self.sio.connect(f"http://{ip}:{PORT}")


def main():
    ClientApp().start()


if __name__ == "__main__":
    main()
