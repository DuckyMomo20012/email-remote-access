from tkinter import messagebox

import socketio


def mac_address(sio: socketio.Client):
    def handleMessage(address: str):
        messagebox.showinfo(title="MAC Address", message=address)

    sio.emit("MAC:info", "", callback=handleMessage)
