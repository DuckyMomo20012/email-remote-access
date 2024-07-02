import dearpygui.dearpygui as dpg


class ConfirmWindow:
    def __init__(self, msg, handleConfirm):
        self.tag = dpg.generate_uuid()

        def handleConfirmClick():
            handleConfirm()

            dpg.delete_item(self.tag)

        with dpg.window(label="Confirm", tag=self.tag, modal=True):
            dpg.add_text(msg)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Yes", callback=handleConfirmClick)
                dpg.add_button(label="No", callback=lambda: dpg.delete_item(self.tag))
