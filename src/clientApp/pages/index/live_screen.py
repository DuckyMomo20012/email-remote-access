import io
import os
import re
from typing import Union

import dearpygui.dearpygui as dpg
import numpy as np
from PIL import Image, ImageGrab

from src.clientApp.app import app
from src.shared.pages.base import BasePage


class LiveScreenWindow(BasePage):
    def __init__(self, parent: Union[int, str], tag: Union[int, str] = "w_live_screen"):
        super().__init__(tag)
        self.parent = parent

        img = ImageGrab.grab().resize((800, 450), Image.Resampling.LANCZOS)
        self.screenHeight = img.height
        self.screenWidth = img.width
        self.frame: bytes
        self.defaultFilename = "screen.png"

        # NOTE: Register the callbacks
        self.callbacks()

    def loadImage(self, data: bytes):
        img = (
            Image.open(io.BytesIO(data))
            .resize((self.screenWidth, self.screenHeight), Image.Resampling.LANCZOS)
            .convert("RGBA")
        )

        dpg_image = np.array(img, dtype="f").flatten() / 255.0

        return dpg_image

    def handleStartStreamClick(self):
        app.sio.emit("LIVESCREEN:start", "")

    def handleStopStreamClick(self):
        app.sio.emit("LIVESCREEN:stop", "")

    def handleSaveFrameClick(self):
        if self.frame is None:
            return

        app.sio.emit("LIVESCREEN:stop", "")

        def handleCancelClick(sender):
            dpg.delete_item(sender)

            app.sio.emit("LIVESCREEN:start", "")

        dpg.add_file_dialog(
            directory_selector=True,
            height=350,
            callback=self.handleSaveFrame,
            cancel_callback=handleCancelClick,
        )

    def handleSaveFrame(self, sender, app_data, user_data):
        for dir in app_data["selections"]:
            # NOTE: Add trailing slash to destPath
            # NOTE: Somehow the last dir is duplicated
            destDir = os.path.join(app_data["selections"][dir].removesuffix(dir), "")
            # NOTE: Remove the number of files selected
            destDir = re.sub(r"(\d+ files Selected){1}.+$", "", destDir)

            if self.frame is None:
                continue

            img = Image.open(io.BytesIO(self.frame))
            img.save(os.path.join(destDir, dir, self.defaultFilename), format="PNG")

        app.sio.emit("LIVESCREEN:start", "")

    def callbacks(self):
        @app.sio.on("LIVESCREEN:stream")
        def stream(data: bytes):
            # NOTE: We save the frame without being resized
            self.frame = data

            dpg_image = self.loadImage(data)

            dpg.set_value("screen", dpg_image)

    def render(self):
        if dpg.does_item_exist("screen"):
            dpg.delete_item("screen")

        with dpg.texture_registry():
            defaultData = np.array(
                [255 / 255] * (self.screenWidth * self.screenHeight * 4), dtype="f"
            )
            dpg.add_raw_texture(
                width=self.screenWidth,
                height=self.screenHeight,
                default_value=defaultData,
                format=dpg.mvFormat_Float_rgba,
                tag="screen",
            )

        with dpg.group(tag=self.tag, parent=self.parent):  # noqa: SIM117
            with dpg.group(horizontal=True):
                dpg.add_button(label="Start", callback=self.handleStartStreamClick)
                dpg.add_button(label="Stop", callback=self.handleStopStreamClick)
                dpg.add_button(label="Save", callback=self.handleSaveFrameClick)

            dpg.add_image("screen")
