import tkinter as tk
from multiprocessing import Process

import psutil

import src.server.server as server


class ServerApp:
    def __init__(self):
        self.main = tk.Tk()
        self.main.geometry("200x200")
        self.main.title("Server")
        self.main["bg"] = "plum1"

        self.start_btn = tk.Button(
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
        )
        self.start_btn.place(x=100, y=100, anchor="center")

    def __del__(self):
        try:
            pid = self.proc.pid
            parent = psutil.Process(pid)
            for child in parent.children(recursive=True):
                child.kill()

            self.proc.terminate()
        except:
            pass

    def start(self):
        self.main.mainloop()

    def connect(self):
        self.proc = Process(target=server.main, daemon=True)
        self.proc.start()

        self.start_btn["state"] = tk.DISABLED


def main():
    app = ServerApp()
    app.start()


if __name__ == "__main__":
    main()
