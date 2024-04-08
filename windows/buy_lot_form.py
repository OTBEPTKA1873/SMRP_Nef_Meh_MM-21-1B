from typing import Iterable, Callable
from datetime import date

from PyQt5.QtWidgets import QWidget, QDialog

from ORM import get_session, User, Seller, Buyer, Lot, Receipt
from ui_qt import UiBuyLotForm
from .dialog import Dialog


class LotBuy(QWidget, UiBuyLotForm):
    def __init__(self, lot: Lot, user: User, callbacks: Iterable[Callable]):
        super().__init__()
        self.lot = lot
        self.buyer = user.buyer
        self.callbacks = callbacks
        self.setupUi(self)
        self.session = get_session()

        self.push_button_buy.clicked.connect(self.buy)
        self.push_button_close.clicked.connect(lambda: self.close())
        self.spinBox_count.valueChanged.connect(self.change_total_price)

        self.label_seller.setText(f"{self.lot.seller.user.last_name} {self.lot.seller.user.first_name} {self.lot.seller.user.patronymic if self.lot.seller.user.patronymic is not None else ''}")
        if self.lot.CPU is not None:
            self.label_component.setText(str(self.lot.CPU.CPU_name))
            # форматные ТХ надо добавить
        elif self.lot.GPU is not None:
            self.label_component.setText(str(self.lot.GPU.GPU_name))
            # ТХ
        elif self.lot.MB is not None:
            self.label_component.setText(str(self.lot.MB.MB_name))
            # ТХ
        elif self.lot.RAM is not None:
            self.label_component.setText(str(self.lot.RAM.RAM_name))
            # ТХ
        elif self.lot.PU is not None:
            self.label_component.setText(str(self.lot.PU.PU_name))
            # ТХ
        elif self.lot.memory is not None:
            self.label_component.setText(str(self.lot.memory.mem_name))
            # ТХ
        else:
            self.label_component.setText(str(self.lot.cooler.cooler_name))
            # ТХ
        self.spinBox_count.setMinimum(1)
        self.spinBox_count.setMaximum(self.lot.count)
        self.label_total_price.settext(str(self.lot.price * self.lot.count))

    def change_total_price(self):
        self.label_total_price.settext(str(self.lot.price * self.lot.count))

    def buy(self):
        buyed_count = self.spinBox_count.value()
        dialog = Dialog("Подтвердите покупку!")
        ret_value = dialog.exec_()
        if ret_value == QDialog.Accepted:
            self.lot.count -= buyed_count
            new_receipt = Receipt(lot_id=self.lot.lot_id,
                                  buyed_count=buyed_count,
                                  buyer_id=self.buyer.buyer_id,
                                  purchase_date=str(date.today()))
            self.session.add(new_receipt)
            self.session.commit()
            self.custom_close()

    def custom_close(self):
        for callback in self.callbacks:
            callback()
        self.close()
