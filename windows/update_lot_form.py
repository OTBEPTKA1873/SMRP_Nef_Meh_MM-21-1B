from typing import Iterable, Callable

from PyQt5.QtWidgets import QWidget, QDialog

from ORM import get_session, User, Lot
from ui_qt import UiUpdateLotForm
from .dialog import Dialog


class LotUpdate(QWidget, UiUpdateLotForm):
    def __init__(self, lot: Lot, user: User, callbacks: Iterable[Callable]):
        super().__init__()
        self.lot = lot
        self.seller = user.seller
        self.callbacks = callbacks
        self.setupUi(self)
        self.session = get_session()

        self.push_button_update.clicked.connect(self.update)
        self.push_button_delete.clicked.connect(self.delete)
        self.push_button_close.clicked.connect(lambda: self.close())

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
        self.line_edit_price.setText(str(self.lot.price))
        self.spinBox.setMinimum(1)
        self.spinBox.setValue(self.lot.count)

    def update(self):
        new_price = float(self.line_edit_price.text())
        new_count = self.spinBox.value()
        if self.seller is not self.lot.seller:
            dialog = Dialog("Нет прав доступа на изменение лота!")
            ret_value = dialog.exec_()
            self.line_edit_price.setText(str(self.lot.price))
            self.line_edit_count.setText(str(self.lot.count))
            return
        if new_price < 0:
            dialog = Dialog("Введены непозволительные данные!")
            ret_value = dialog.exec_()
            self.line_edit_price.setText(str(self.lot.price))
            self.line_edit_count.setText(str(self.lot.count))
            return
        dialog = Dialog("Подтвердите обновление лота!")
        ret_value = dialog.exec_()
        if ret_value == QDialog.Accepted:
            lot_to_update: Lot = self.session.query(Lot).get(self.lot.lot_id)
            lot_to_update.price = new_price
            lot_to_update.count = new_count
            self.session.commit()
            self.custom_close()

    def delete(self):
        if self.seller is not self.lot.seller:
            dialog = Dialog("Нет прав доступа на удаление лота!")
            ret_value = dialog.exec_()
            self.line_edit_price.setText(str(self.lot.price))
            self.line_edit_count.setText(str(self.lot.count))
            return
        dialog = Dialog("Подтвердите удаление лота!")
        ret_value = dialog.exec_()
        if ret_value == QDialog.Accepted:
            lot_to_delete: Lot = self.session.query(Lot).get(self.lot.lot_id)
            self.session.delete(lot_to_delete)
            self.session.commit()
            self.custom_close()

    def custom_close(self):
        for callback in self.callbacks:
            callback()
        self.close()
