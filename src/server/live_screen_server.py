# Socket
import io
import threading

import socketio

# Work with Image
from PIL import ImageGrab


class StreamHandler:
    _isStreaming: bool
    lock: threading.Lock

    def __init__(self):
        self._isStreaming = False
        self.lock = threading.Lock()

    @property
    def isStreaming(self):
        return self._isStreaming

    @isStreaming.setter
    def isStreaming(self, data):
        self.lock.acquire()
        self._isStreaming = data
        self.lock.release()

    def stream(self):
        while self.isStreaming:
            img = ImageGrab.grab()
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            data = img_bytes.getvalue()

            yield data


def callbacks(sio: socketio.AsyncServer):
    @sio.on("LIVESCREEN:start")
    async def on_stream(sid, data):
        handler = StreamHandler()

        handler.isStreaming = True

        @sio.on("LIVESCREEN:stop")
        def on_stream_stop(sid, data):
            handler.isStreaming = False

        for data in handler.stream():
            await sio.emit("LIVESCREEN:stream", data, to=sid)

    @sio.on("LIVESCREEN:screenshot")
    def on_screenshot(sid, data):
        img = ImageGrab.grab()
        imgBytesIO = io.BytesIO()
        img.save(imgBytesIO, format="PNG")
        imgBytes = imgBytesIO.getvalue()

        return imgBytes, None
