import tkinter as tk

import socketio


def close_event(main: tk.Toplevel, sio: socketio.Client):
    sio.emit("QUIT")
    main.destroy()
    return


def shutdown(sio: socketio.Client):
    sio.emit("SD_LO:shutdown")


def logout(sio: socketio.Client):
    sio.emit("SD_LO:logout")


def shutdown_logout(sio: socketio.Client, root: tk.Tk):
    window = tk.Toplevel(root)
    window.geometry("190x160")
    window.grab_set()
    window.protocol("WM_DELETE_WINDOW", lambda: close_event(window, sio))
    shutdown_btn = tk.Button(
        window,
        text="SHUTDOWN",
        width=20,
        height=2,
        fg="white",
        bg="IndianRed3",
        command=lambda: shutdown(sio),
        padx=20,
        pady=20,
    )
    shutdown_btn.grid(row=0, column=0)
    logout_btn = tk.Button(
        window,
        text="LOGOUT",
        width=20,
        height=2,
        fg="white",
        bg="royalblue4",
        command=lambda: logout(sio),
        padx=20,
        pady=20,
    )
    logout_btn.grid(row=1, column=0)
    window.mainloop()
