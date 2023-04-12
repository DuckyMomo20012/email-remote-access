from tkinter import messagebox

import socketio


def mac_address(sio: socketio.Client):
    def handleMessage(address: str):
        address = address[2:].upper()
        address = ":".join(address[i : i + 2] for i in range(0, len(address), 2))
        messagebox.showinfo(title="MAC Address", message=address)

    sio.emit("MAC:info", "", callback=handleMessage)
