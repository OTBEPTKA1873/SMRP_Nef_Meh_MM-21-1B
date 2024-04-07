from typing import Iterable, Callable

from PyQt5.QtWidgets import QWidget

from ORM import get_session, Lot, User
from ui_qt import UiAddLotForm


class LotAdd(QWidget, UiAddLotForm):
    def __init__(self, callbacks: Iterable[Callable]):
        super().__init__()
        self.callbacks = callbacks
        self.setupUi(self)
        self.session = get_session()
        self.push_button_create.clicked.connect(self.create_lot)
        self.push_button_close.clicked.connect(lambda: self.close())

    def create_lot(self):
        ...
        self.session.add()
        self.session.commit()

        self.custom_close()

    def custom_close(self):
        for callback in self.callbacks:
            callback()
        self.close()
