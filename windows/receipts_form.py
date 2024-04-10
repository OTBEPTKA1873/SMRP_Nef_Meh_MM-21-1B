from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from ORM import get_session, User, Seller, Buyer, Lot, Receipt
from ui_qt import UiReceiptsForm


class Receipts(QWidget, UiReceiptsForm):
    def __init__(self, user: User):
        super().__init__()
        self.user = user
        self.setupUi(self)
        self.session = get_session()

        self.pushButton.clicked.connect(lambda: self.close())

        """
        receipts = self.session.query(Receipt).where(Receipt.lot.seller.user.user_id == self.user.user_id or Receipt.buyer_id == buyer.buyer_id).order_by(Receipt.purchase_date).all()
        self.tableWidget.setRowCount(0)
        for receipt in receipts:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setItem(row_position, 0, QTableWidgetItem(receipt.purchase_date))
            self.tableWidget.setItem(row_position, 1, QTableWidgetItem(
                f"{receipt.buyer.user.last_name} {receipt.buyer.user.first_name} {receipt.buyer.user.patronymic if receipt.buyer.user.patronymic else ''}"))
            self.tableWidget.setItem(row_position, 2, QTableWidgetItem(
                f"{receipt.lot.seller.user.last_name} {receipt.lot.seller.user.first_name} {receipt.lot.seller.user.patronymic if receipt.lot.seller.user.patronymic else ''}"))
            self.tableWidget.setItem(row_position, 3, QTableWidgetItem(receipt.lot.component_name()))
            self.tableWidget.setItem(row_position, 4, QTableWidgetItem(str(receipt.lot.price)))
        """
        self.session.close()
