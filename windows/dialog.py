from PyQt5.QtWidgets import QDialog

from ui_qt import UiDialog


class Dialog(QDialog, UiDialog):
    def __init__(self, text: str):
        super().__init__()
        self.setupUi(self)
        self.textBrowser.setText(text)
