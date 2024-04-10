from typing import Iterable, Callable
from datetime import date

from PyQt5.QtWidgets import QWidget, QDialog

from ORM import get_session, User, Buyer, Lot, Receipt
from ui_qt import UiBuyLotForm
from .dialog import Dialog


class LotBuy(QWidget, UiBuyLotForm):
    def __init__(self, lot: Lot, user: User, callbacks: Iterable[Callable]):
        super().__init__()
        self.lot = lot
        self.callbacks = callbacks
        self.setupUi(self)
        self.session = get_session()
        self.buyer = self.session.query(Buyer).where(Buyer.user_id == user.user_id).one()

        self.push_button_buy.clicked.connect(self.buy)
        self.push_button_close.clicked.connect(lambda: self.close())
        self.spinBox_count.valueChanged.connect(self.change_total_price)

        self.label_seller.setText(f"{self.lot.seller.user.last_name} {self.lot.seller.user.first_name} {self.lot.seller.user.patronymic if self.lot.seller.user.patronymic is not None else ''}")
        self.label_component.setText(self.lot.component_name())
        self.label_charac.setText(self.lot.component_TC())
        self.spinBox_count.setMinimum(1)
        self.spinBox_count.setMaximum(self.lot.count)
        self.label_total_price.setText(str(self.lot.price * self.spinBox_count.value()))

    def change_total_price(self):
        self.label_total_price.setText(str(self.lot.price * self.spinBox_count.value()))

    def buy(self):
        buyed_count = self.spinBox_count.value()
        dialog = Dialog("Подтвердите покупку!")
        ret_value = dialog.exec_()
        if ret_value == QDialog.Accepted:
            buyed_lot = self.session.query(Lot).get(self.lot.lot_id)
            buyed_lot.count -= buyed_count
            # self.lot.count -= buyed_count
            new_receipt = Receipt(lot_id=self.lot.lot_id,
                                  buyed_count=buyed_count,
                                  buyer_id=self.buyer.buyer_id,
                                  purchase_date=str(date.today()))
            self.session.add(new_receipt)
            self.session.commit()
            self.session.close()
            self.custom_close()

    def custom_close(self):
        for callback in self.callbacks:
            callback()
        self.close()
