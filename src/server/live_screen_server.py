# Socket
import io

import socketio

# Work with Image
from PIL import ImageGrab


def callbacks(sio: socketio.AsyncServer):
    @sio.on("LIVESCREEN:start")
    async def on_stream(sid, data):
        isStreaming = True

        @sio.on("LIVESCREEN:stop")
        def on_stream_stop(sid, data):
            nonlocal isStreaming
            isStreaming = False

        while isStreaming:
            img = ImageGrab.grab()
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            data = img_bytes.getvalue()

            await sio.emit("LIVESCREEN:stream", data)

    @sio.on("LIVESCREEN:screenshot")
    def on_screenshot(sid, data):
        img = ImageGrab.grab()
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_content = img_bytes.getvalue()

        return img_content
