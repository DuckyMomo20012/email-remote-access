import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Button, Canvas, PhotoImage, Text, filedialog, messagebox
from typing import Dict

import socketio

SEPARATOR = "<SEPARATOR>"


def abs_path(file_name):
    file_name = "assets\\" + file_name
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, file_name)


class DirectoryTree_UI(Canvas):
    def __init__(self, parent, sio: socketio.Client):
        Canvas.__init__(self, parent)
        self.sio = sio
        self.currPath = " "
        self.nodes: Dict[str, str] = dict()

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
        self.image_image_1 = PhotoImage(file=abs_path("bg.png"))
        self.image_1 = self.create_image(519.0, 327.0, image=self.image_image_1)

        self.frame = tk.Frame(self, height=200, width=500)
        self.tree = ttk.Treeview(self.frame)
        self.frame.place(x=53.0, y=162.0, width=713.0, height=404.0)

        self.insText1 = "Click SHOW button to show the server's directory tree."
        self.label1 = tk.Label(self.frame, text=self.insText1)
        self.label1.pack(fill=tk.X)

        ysb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        xsb = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
        self.tree.heading("#0", text="Server's Directory Tree", anchor="w")
        self.tree.pack(fill=tk.BOTH)

        self.tree.bind("<<TreeviewOpen>>", self.open_node)
        self.tree.bind("<<TreeviewSelect>>", self.select_node)

        self.insText2 = (
            "Selected path.\n"
            "Click SEND FILE TO FOLDER button to select a file you want to copy to"
            "this folder.\n"
            "Click COPY THIS FILE to copy the selected file to your computer"
            "(client)\n"
            "Click DELETE button to delete the file on this path.\nYou can click SHOW"
            "button again to see the changes."
        )
        self.label2 = tk.Label(self.frame, text=self.insText2)
        self.label2.pack(fill=tk.X)
        self.path = Text(self.frame, height=1, width=26, state="disabled")
        self.path.pack(fill=tk.X)
        self.button_2 = Button(
            self,
            text="SHOW",
            width=20,
            height=5,
            fg="white",
            bg="IndianRed3",
            # image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.showTree,
            relief="flat",
        )
        self.button_2.place(x=838.0, y=152.0, width=135.0, height=53.0)
        self.button_3 = Button(
            self,
            text="SEND FILE TO FOLDER",
            width=20,
            height=5,
            fg="white",
            bg="IndianRed3",
            # image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.copyFileToServer,
            relief="flat",
        )
        self.button_3.place(x=838.0, y=238.0, width=135.0, height=53.0)
        self.button_4 = Button(
            self,
            text="COPY THIS FILE",
            width=20,
            height=5,
            fg="white",
            bg="IndianRed3",
            # image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.copyFileToClient,
            relief="flat",
        )
        self.button_4.place(x=838.0, y=317.0, width=135.0, height=53.0)
        self.button_5 = Button(
            self,
            text="DELETE",
            width=20,
            height=5,
            fg="white",
            bg="IndianRed3",
            # image=button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.deleteFile,
            relief="flat",
        )
        self.button_5.place(x=839.0, y=396.0, width=135.0, height=53.0)
        self.button_6 = Button(
            self,
            text="BACK",
            width=20,
            height=5,
            fg="white",
            bg="IndianRed3",
            # image=button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.back(),
            relief="flat",
        )
        self.button_6.place(x=838.0, y=473.0, width=135.0, height=53.0)

    def insert_node(self, parent, text, abspath, isFolder):
        node = self.tree.insert(parent, "end", text=text, open=False)
        if abspath != "" and isFolder:
            self.nodes[node] = abspath
            self.tree.insert(node, "end")

    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            try:
                self.listDirs(node, abspath)
            except Exception:
                messagebox.showerror(message="Cannot open this directory!")

    def select_node(self, event):
        item = self.tree.selection()[0]
        parent = self.tree.parent(item)
        self.currPath = self.tree.item(item, "text")
        while parent:
            self.currPath = os.path.join(self.tree.item(parent)["text"], self.currPath)
            item = parent
            parent = self.tree.parent(item)

        self.path.config(state="normal")
        self.path.delete("1.0", tk.END)
        self.path.insert(tk.END, self.currPath)
        self.path.config(state="disabled")

    def deleteTree(self):
        self.currPath = " "
        self.path.config(state="normal")
        self.path.delete("1.0", tk.END)
        self.path.config(state="disabled")
        for i in self.tree.get_children():
            self.tree.delete(i)

    def showTree(self):
        self.deleteTree()
        self.sio.emit("DIRECTORY:show_tree")

        @self.sio.on("DIRECTORY:show_tree:data")
        def showTreeData(data):
            for path in data:
                try:
                    abspath = os.path.abspath(path)
                    self.insert_node("", abspath, abspath, True)
                except Exception:
                    continue

    def listDirs(self, node, path):
        self.sio.emit("DIRECTORY:list_dirs", path)

        @self.sio.on("DIRECTORY:list_dirs:data")
        def listDirsData(data):
            for p in data:
                self.insert_node(node, p[0], os.path.join(path, p[0]), p[1])

        @self.sio.on("DIRECTORY:list_dirs:error")
        def listDirsError():
            messagebox.showerror(message="Cannot open this directory!")

    # copy file from client to server
    def copyFileToServer(self):
        filename = filedialog.askopenfilename(
            title="Select File", filetypes=[("All Files", "*.*")]
        )
        if filename is None or filename == "":
            return
        destPath = self.currPath + "\\"
        filesize = os.path.getsize(filename)
        self.sio.emit(
            "DIRECTORY:copyto",
            {
                "metadata": f"{filename}{SEPARATOR}{filesize}{SEPARATOR}{destPath}",
                "data": open(filename, "rb").read(),
            },
        )

        @self.sio.on("DIRECTORY:copyto:status")
        def copyFileToServerStatus(data):
            if data == "OK":
                messagebox.showinfo(message="Copy file successfully!")
            else:
                messagebox.showerror(message="Cannot copy file!")

    # copy file from server to client
    def copyFileToClient(self):
        destPath = filedialog.askdirectory()
        if destPath is None or destPath == "":
            return

        self.sio.emit(
            "DIRECTORY:copy",
            self.currPath,
        )

        @self.sio.on("DIRECTORY:copy:data")
        def copyFileToClientData(data):
            with open(os.path.abspath(destPath) + "\\" + data["filename"], "wb") as f:
                f.write(data["fileData"])

            messagebox.showinfo(message="Copy file successfully!")

        @self.sio.on("DIRECTORY:copy:error")
        def copyFileToClientError():
            messagebox.showerror(message="Cannot copy file!")

    def deleteFile(self):
        self.sio.emit("DIRECTORY:delete", self.currPath)

        @self.sio.on("DIRECTORY:delete:status")
        def deleteFileStatus(data):
            if data == "OK":
                messagebox.showinfo(message="Delete file successfully!")
            else:
                messagebox.showerror(message="Cannot delete file!")

    def back(self):
        return
