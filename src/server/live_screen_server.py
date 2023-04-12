# Socket
import io

import socketio

# Work with Image
from PIL import ImageGrab


def callbacks(sio: socketio.AsyncServer):
    @sio.on("LIVESCREEN:start")
    async def on_stream(sid):
        isStreaming = True

        @sio.on("LIVESCREEN:stop")
        def on_stream_stop(sid):
            nonlocal isStreaming
            isStreaming = False

        while isStreaming:
            img = ImageGrab.grab()
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            data = img_bytes.getvalue()

            await sio.emit("LIVESCREEN:stream", data)

    @sio.on("LIVESCREEN:screenshot")
    async def on_screenshot(sid):
        img = ImageGrab.grab()
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        data = img_bytes.getvalue()

        await sio.emit("LIVESCREEN:screenshot:data", data)
