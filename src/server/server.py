import socket
import tkinter as tk

# import keylogger_server as kl
import src.server.app_process_server as ap
import src.server.directory_tree_server as dt
import src.server.live_screen_server as lss
import src.server.mac_address_server as mac
import src.server.registry_server as rs
import src.server.shutdown_logout_server as sl

BUFSIZ = 1024 * 4


class Server:
    def __init__(self):
        self.main = tk.Tk()
        self.main.geometry("200x200")
        self.main.title("Server")
        self.main["bg"] = "plum1"

        tk.Button(
            self.main,
            text="OPEN",
            width=10,
            height=2,
            fg="white",
            bg="IndianRed3",
            borderwidth=0,
            highlightthickness=0,
            command=self.connect,
            relief="flat",
        ).place(x=100, y=100, anchor="center")

    def start(self):
        self.main.mainloop()

    def keylogger(self, client):
        # global client
        # kl.keylog(client)
        return

    def shutdown_logout(self, client):
        # global client
        sl.shutdown_logout(client)
        return

    def mac_address(self, client):
        # global client
        mac.mac_address(client)
        return

    def app_process(self, client):
        # global client
        ap.app_process(client)
        return

    def live_screen(self, client):
        # global client
        lss.capture_screen(client)
        return
        return

    def directory_tree(self, client):
        # global client
        dt.directory(client)
        return

    def registry(self, client):
        # global client
        rs.registry(client)
        return

    # Connect
    ###############################################################################
    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ""
        port = 5656
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(100)
        # global client
        client, addr = s.accept()
        while True:
            msg = client.recv(BUFSIZ).decode("utf8")
            if "KEYLOG" in msg:
                self.keylogger(client)
            elif "SD_LO" in msg:
                self.shutdown_logout(client)
            elif "LIVESCREEN" in msg:
                self.live_screen(client)
            elif "APP_PRO" in msg:
                self.app_process(client)
            elif "MAC" in msg:
                self.mac_address(client)
            elif "DIRECTORY" in msg:
                self.directory_tree(client)
            elif "REGISTRY" in msg:
                self.registry(client)
            elif "QUIT" in msg:
                client.close()
                s.close()
                return


###############################################################################


def main():
    Server().start()


if __name__ == "__main__":
    main()
