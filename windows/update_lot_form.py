from typing import Iterable, Callable

from PyQt5.QtWidgets import QWidget, QDialog

from ORM import get_session, User, Lot, Seller, Receipt
from ui_qt import UiUpdateLotForm
from .dialog import Dialog


class LotUpdate(QWidget, UiUpdateLotForm):
    def __init__(self, lot: Lot, user: User, callbacks: Iterable[Callable]):
        super().__init__()
        self.lot = lot
        self.callbacks = callbacks
        self.setupUi(self)
        self.session = get_session()
        if user is not None:
            self.seller = self.session.query(Seller).where(Seller.user_id == user.user_id).one()
        else:
            self.seller = None

        self.push_button_update.clicked.connect(self.update)
        self.push_button_delete.clicked.connect(self.delete)
        self.push_button_close.clicked.connect(lambda: self.close())

        self.label_seller.setText(f"{self.lot.seller.user.last_name} {self.lot.seller.user.first_name} {self.lot.seller.user.patronymic if self.lot.seller.user.patronymic is not None else ''}")
        self.label_component.setText(self.lot.component_name())
        self.label_charac.setText(self.lot.component_TC())
        self.line_edit_price.setText(str(self.lot.price))
        self.spinBox.setMinimum(1)
        self.spinBox.setValue(self.lot.count)

    def update(self):
        new_count = self.spinBox.value()
        if self.seller is None:
            dialog = Dialog("Нет прав доступа на изменение лота!")
            ret_value = dialog.exec_()
            self.line_edit_price.setText(str(self.lot.price))
            self.spinBox.setValue(self.lot.count)
            return
        if self.seller.seller_id != self.lot.seller.seller_id:
            dialog = Dialog("Нет прав доступа на изменение лота!")
            ret_value = dialog.exec_()
            self.line_edit_price.setText(str(self.lot.price))
            self.spinBox.setValue(self.lot.count)
            return
        if not self.line_edit_price.text().isdigit():
            dialog = Dialog("Введены непозволительные данные!")
            ret_value = dialog.exec_()
            self.line_edit_price.setText(str(self.lot.price))
            self.spinBox.setValue(self.lot.count)
            return
        new_price = float(self.line_edit_price.text())
        if new_price < 0:
            dialog = Dialog("Введены непозволительные данные!")
            ret_value = dialog.exec_()
            self.line_edit_price.setText(str(self.lot.price))
            self.spinBox.setValue(self.lot.count)
            return
        dialog = Dialog("Подтвердите обновление лота!")
        ret_value = dialog.exec_()
        if ret_value == QDialog.Accepted:
            lot_to_update: Lot = self.session.query(Lot).get(self.lot.lot_id)
            lot_to_update.price = new_price
            lot_to_update.count = new_count
            self.session.commit()
            self.session.close()
            self.custom_close()
        else:
            self.line_edit_price.setText(str(self.lot.price))
            self.spinBox.setValue(self.lot.count)

    def delete(self):
        if self.seller is None:
            dialog = Dialog("Нет прав доступа на удаление лота!")
            ret_value = dialog.exec_()
            self.line_edit_price.setText(str(self.lot.price))
            self.spinBox.setValue(self.lot.count)
            return
        if self.seller.seller_id != self.lot.seller.seller_id:
            dialog = Dialog("Нет прав доступа на удаление лота!")
            ret_value = dialog.exec_()
            self.line_edit_price.setText(str(self.lot.price))
            self.spinBox.setValue(self.lot.count)
            return
        dialog = Dialog("Подтвердите удаление лота!")
        ret_value = dialog.exec_()
        if ret_value == QDialog.Accepted:
            lot_to_delete: Lot = self.session.query(Lot).get(self.lot.lot_id)
            lots_in_receipts = [receipt.lot for receipt in self.session.query(Receipt).all()]
            if lot_to_delete in lots_in_receipts:
                lot_to_delete.count = 0
            else:
                self.session.delete(lot_to_delete)
            self.session.commit()
            self.session.close()
            self.custom_close()
        else:
            self.line_edit_price.setText(str(self.lot.price))
            self.spinBox.setValue(self.lot.count)

    def custom_close(self):
        for callback in self.callbacks:
            callback()
        self.close()
