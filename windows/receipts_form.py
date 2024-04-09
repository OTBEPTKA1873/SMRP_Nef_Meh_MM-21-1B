from PyQt5.QtWidgets import QWidget

from ORM import get_session, User, Seller, Buyer, Lot, Receipt
from ui_qt import UiReceiptsForm


class LotBuy(QWidget, UiReceiptsForm):
    def __init__(self, user: User):
        super().__init__()
        self.user = user
        self.setupUi(self)
        self.session = get_session()

        self.pushButton.clicked.connect(lambda: self.close())

        # заполнить таблицу


