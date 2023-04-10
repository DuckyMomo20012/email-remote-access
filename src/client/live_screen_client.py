# Socket
import io

# Tkinter
import tkinter as tk

# Thread
from threading import Thread
from tkinter import Canvas
from tkinter.filedialog import asksaveasfile

import socketio

# Image
from PIL import Image, ImageTk


class Desktop_UI(Canvas):
    def __init__(self, parent: tk.Tk, sio: socketio.Client):
        Canvas.__init__(self, parent)
        self.configure(
            # window,
            bg="#FCD0E8",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.place(x=0, y=0)

        # copy socket connection to own attribute
        self.sio = sio

        # initialize status to ready receiving data
        self.status = True

        # initialize the sentinel of saving image command
        self.on_save = False

        # label to display frames received from server
        self.label = tk.Label(self)
        self.label.place(x=20, y=0, width=960, height=540)

        # a button to save captured screen
        self.btn_save = tk.Button(
            self, text="Save", command=lambda: self.click_save(), relief="flat"
        )
        self.btn_save.place(x=320, y=560, width=50, height=30)

        # a button to stop receiving and return to main interface
        self.btn_back = tk.Button(
            self, text="Back", command=lambda: self.click_back(), relief="flat"
        )
        self.btn_back.place(x=630, y=560, width=50, height=30)

        # thread
        self.start = Thread(target=self.ChangeImage, daemon=True)
        self.start.start()

    # display frames continously
    def ChangeImage(self):
        @self.sio.on("LIVESCREEN:stream")
        def stream(data):
            img_PIL = Image.open(io.BytesIO(data)).resize((960, 540), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(img_PIL)
            self.label.configure(image=img_tk)
            self.label.image = img_tk

            self.frame = data

    def click_back(self):
        self.status = False

        self.sio.emit("LIVESCREEN:stop")

        self.place_forget()

    def click_save(self):
        self.on_save = True
        self.sio.emit("LIVESCREEN:stop")

        self.save_img()
        self.on_save = False
        self.sio.emit("LIVESCREEN:start")

    def save_img(self):
        if self.frame is None:
            return

        types = [("Portable Network Graphics", "*.png"), ("All Files", "*.*")]
        img_file = asksaveasfile(mode="wb", filetypes=types, defaultextension="*.png")
        if img_file is None:
            return
        img_file.write(self.frame)
