# Socket
import io

import socketio

# Work with Image
from PIL import ImageGrab


async def capture_screen(sio: socketio.AsyncServer):
    isStreaming = True

    @sio.on("LIVESCREEN:stop")
    def stop(sid):
        nonlocal isStreaming
        isStreaming = False

    while isStreaming:
        img = ImageGrab.grab()
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        data = img_bytes.getvalue()

        await sio.emit("LIVESCREEN:stream", data)
