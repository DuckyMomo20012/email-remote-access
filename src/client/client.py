import socket
import tkinter as tk

import src.client.app_process_client as ap
import src.client.directory_tree_client as dt
import src.client.entrance_ui as ui1
import src.client.keylogger_client as kl
import src.client.live_screen_client as lsc
import src.client.mac_address_client as mac
import src.client.main_ui as ui2
import src.client.registry_client as rc
import src.client.shutdown_logout_client as sl

BUFSIZ = 1024 * 4


class Client:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x600")
        self.root.configure(bg="#FFFFFF")
        self.root.title("Client")
        self.root.resizable(False, False)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.f1 = ui1.Entrance_UI(self.root)
        self.f1.button_1.configure(command=self.connect)

    def start(self):
        self.root.mainloop()

    def back(self, ui):
        ui.place_forget()
        f2.place(x=0, y=0)
        self.client.sendall(bytes("QUIT", "utf8"))

    def live_screen(self):
        self.client.sendall(bytes("LIVESCREEN", "utf8"))
        tmp = lsc.Desktop_UI(self.root, self.client)
        if not tmp.status:
            self.back(tmp)
        return

    def shutdown_logout(self):
        self.client.sendall(bytes("SD_LO", "utf8"))
        sl.shutdown_logout(self.client, self.root)
        return

    def mac_address(self):
        self.client.sendall(bytes("MAC", "utf8"))
        mac.mac_address(self.client)
        return

    def back_dirTree(self, ui):
        ui.place_forget()
        ui.tree.pack_forget()
        f2.place(x=0, y=0)
        self.client.sendall(bytes("QUIT", "utf8"))

    def directory_tree(self):
        self.client.sendall(bytes("DIRECTORY", "utf8"))
        tmp = dt.DirectoryTree_UI(self.root, self.client)
        tmp.button_6.configure(command=lambda: self.back_dirTree(tmp))
        return

    def app_process(self):
        self.client.sendall(bytes("APP_PRO", "utf8"))
        tmp = ap.App_Process_UI(self.root, self.client)
        tmp.button_6.configure(command=lambda: self.back(tmp))
        return

    def disconnect(self):
        f2.place_forget()
        self.f1.place(x=0, y=0)
        self.client.sendall(bytes("QUIT", "utf8"))
        return

    def keylogger(self):
        self.client.sendall(bytes("KEYLOG", "utf8"))
        tmp = kl.Keylogger_UI(self.root, self.client)
        tmp.button_6.configure(command=lambda: self.back(tmp))
        return

    def registry(self):
        self.client.sendall(bytes("REGISTRY", "utf8"))
        tmp = rc.Registry_UI(self.root, self.client)
        tmp.btn_back.configure(command=lambda: self.back_reg(tmp))
        return

    def back_reg(self, ui):
        ui.client.sendall(bytes("STOP_EDIT_REGISTRY", "utf8"))
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

    def connect(self):
        # global client
        ip = self.f1.input.get()
        try:
            self.client.connect((ip, 5656))
            tk.messagebox.showinfo(message="Connect successfully!")
            self.show_main_ui()
        except:
            tk.messagebox.showerror(message="Cannot connect!")
        return


def main():
    Client().start()


if __name__ == "__main__":
    main()
