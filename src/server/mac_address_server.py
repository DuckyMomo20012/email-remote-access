import uuid


async def mac_address(sio):
    await sio.emit(
        "MAC:info",
        bytes(hex(uuid.getnode()), "utf8"),
    )
    return
