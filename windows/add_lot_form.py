from typing import Iterable, Callable

from PyQt5.QtWidgets import QWidget, QDialog, QTableWidget, QTableWidgetItem

from ORM import get_session, Lot, User, CPU, MB, GPU, Cooler, RAM, Memory, PU, Seller
from ui_qt import UiAddLotForm
from .dialog import Dialog


class LotAdd(QWidget, UiAddLotForm):

    def __init__(self, current_user: User, callbacks: Iterable[Callable]):
        super().__init__()

        self.component_id_dict = {}  # Создаем словарь для id
        self.callbacks = callbacks
        self.setupUi(self)
        self.session = get_session()
        self.seller = self.session.query(Seller).where(Seller.user_id == current_user.user_id).one()
        self.index = 0

        self.push_button_close.clicked.connect(lambda: self.close())  # Закрытие окна
        self.comboBox.activated.connect(self.activated)  # Вызов функции activated
        self.push_button_create.clicked.connect(self.create_lot)
        self.spinBox.setMinimum(1)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3)

    def activated(self, index):
        self.index = index
        self.tableWidget.setRowCount(0)
        self.component_id_dict.clear()
        if index == 1:
            cpu = self.session.query(CPU).all()
            for i in cpu:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.CPU_name))  # Заполняем название
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(f"{i.ALU} Ядер,  {i.freq} Гц,  {i.socket}, Тепловыделение: {i.TDP} Вт"))
                self.component_id_dict[rowPosition] = i.CPU_id
        elif index == 2:
            mb = self.session.query(MB).all()
            for i in mb:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.MB_name))  # Заполняем название
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(f"{i.form_factor},  {i.socket_type},  {i.RAM_type}x{i.RAM_count},  {i.freq} Гц,  {i.GPU_type}"))
                self.component_id_dict[rowPosition] = i.MB_id
        elif index == 3:
            gpu = self.session.query(GPU).all()
            for i in gpu:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.GPU_name))  # Заполняем название
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(f"{i.freq} Гц,  {i.ALU} Ядер,  {i.volume} Гб,  {i.GPU_type}"))
                self.component_id_dict[rowPosition] = i.GPU_id
        elif index == 4:
            cooler = self.session.query(Cooler).all()
            for i in cooler:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.cooler_name))  # Заполняем название
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(f"{i.socket},  {i.DH} Вт,  {i.noise} Дб"))
                self.component_id_dict[rowPosition] = i.cooler_id
        elif index == 5:
            ram = self.session.query(RAM).all()
            for i in ram:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.RAM_name))  # Заполняем название
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(f"{i.RAM_type},  {i.volume} Гб,  {i.freq} Гц"))
                self.component_id_dict[rowPosition] = i.RAM_id
        elif index == 6:
            mem = self.session.query(Memory).all()
            for i in mem:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.mem_name))  # Заполняем название
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(f"{i.mem_type},  {i.volume} Гб, скорость: {i.speed} Мб/с"))
                self.component_id_dict[rowPosition] = i.mem_id
        elif index == 7:
            pu = self.session.query(PU).all()
            for i in pu:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.PU_name))  # Заполняем название
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(f"{i.watt} Вт"))
                self.component_id_dict[rowPosition] = i.PU_id

    def create_lot(self):
        if self.index == 0:
            dialog = Dialog("Выберите тип комплектующего!")
            dialog.exec_()
            return
        if self.tableWidget.currentRow() < 0:
            dialog = Dialog("Выберите, что продавать!")
            dialog.exec_()
            return
        if len(self.line_edit_price.text()) == 0:
            dialog = Dialog("Укажите цену!")
            dialog.exec_()
            return
        if not self.line_edit_price.text().isdigit():
            dialog = Dialog("Введены непозволительные данные!")
            dialog.exec_()
            return

        dialog = Dialog("Подтвердите создание лота!")
        ret_value = dialog.exec_()
        if ret_value == QDialog.Accepted:
            component = self.comboBox.currentIndex()
            if component == 1: # Создание лота CPU
                new_lot = Lot(seller_id=self.seller.seller_id,
                              price=self.line_edit_price.text(),
                              GPU_id=None,
                              CPU_id=self.component_id_dict[self.tableWidget.currentRow()],
                              MB_id=None,
                              RAM_id=None,
                              PU_id=None,
                              mem_id=None,
                              cooler_id=None,
                              count=self.spinBox.value())
                self.session.add(new_lot)
                self.session.commit()
            elif component == 2: # Создание лота MB
                new_lot = Lot(seller_id=self.seller.seller_id,
                             price=self.line_edit_price.text(),
                             GPU_id=None,
                             CPU_id=None,
                             MB_id=self.component_id_dict[self.tableWidget.currentRow()],
                             RAM_id=None,
                             PU_id=None,
                             mem_id=None,
                             cooler_id=None,
                             count=self.spinBox.value())
                self.session.add(new_lot)
                self.session.commit()
            elif component == 3: # Создание лота GPU
                new_lot = Lot(seller_id=self.seller.seller_id,
                             price=self.line_edit_price.text(),
                             GPU_id=self.component_id_dict[self.tableWidget.currentRow()],
                             CPU_id=None,
                             MB_id=None,
                             RAM_id=None,
                             PU_id=None,
                             mem_id=None,
                             cooler_id=None,
                             count=self.spinBox.value())
                self.session.add(new_lot)
                self.session.commit()
            elif component == 4: # Создание лота cooler
                new_lot = Lot(seller_id=self.seller.seller_id,
                             price=self.line_edit_price.text(),
                             GPU_id=None,
                             CPU_id=None,
                             MB_id=None,
                             RAM_id=None,
                             PU_id=None,
                             mem_id=None,
                             cooler_id=self.component_id_dict[self.tableWidget.currentRow()],
                             count=self.spinBox.value())
                self.session.add(new_lot)
                self.session.commit()
            elif component == 5: # Создание лота RAM
                new_lot = Lot(seller_id=self.seller.seller_id,
                             price=self.line_edit_price.text(),
                             GPU_id=None,
                             CPU_id=None,
                             MB_id=None,
                             RAM_id=self.component_id_dict[self.tableWidget.currentRow()],
                             PU_id=None,
                             mem_id=None,
                             cooler_id=None,
                             count=self.spinBox.value())
                self.session.add(new_lot)
                self.session.commit()
            elif component == 6: # Создание лота memory
                new_lot = Lot(seller_id=self.seller.seller_id,
                             price=self.line_edit_price.text(),
                             GPU_id=None,
                             CPU_id=None,
                             MB_id=None,
                             RAM_id=None,
                             PU_id=None,
                             mem_id=self.component_id_dict[self.tableWidget.currentRow()],
                             cooler_id=None,
                             count=self.spinBox.value())
                self.session.add(new_lot)
                self.session.commit()
            elif component == 7: # Создание лота PU
                new_lot = Lot(seller_id=self.seller.seller_id,
                             price=self.line_edit_price.text(),
                             GPU_id=None,
                             CPU_id=None,
                             MB_id=None,
                             RAM_id=None,
                             PU_id=self.component_id_dict[self.tableWidget.currentRow()],
                             mem_id=None,
                             cooler_id=None,
                             count=self.spinBox.value())
                self.session.add(new_lot)
                self.session.commit()
            self.custom_close()

    def custom_close(self):
        for callback in self.callbacks:
            callback()
        self.close()
