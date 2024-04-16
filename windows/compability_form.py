from typing import Iterable, Callable

from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem

from ORM import get_session, CPU, MB, GPU, Cooler, RAM
from ui_qt import UiCompability


class Compability(QWidget, UiCompability):

    def __init__(self):
        super().__init__()

        self.component_id_dict = {}  # Создаем словарь для id
        self.setupUi(self)
        self.session = get_session()
        self.index = 0

        self.componentBox.connect(self.activated)
        self.compo.activated.connect(self.activated)  # Вызов функции activated
        self.pushButton.clicked.connect(self.check_compability)
        self.componentTable.horizontalHeader().setSectionResizeMode(3)

    def activated(self, index):
        self.index = index
        self.componentTable.setRowCount(0)
        self.component_id_dict.clear()
        if index == 1:
            cpu = self.session.query(CPU).all()
            for i in cpu:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.CPU_name))  # Заполняем название
                self.component_id_dict[rowPosition] = i.CPU_id
        elif index == 2:
            gpu = self.session.query(GPU).all()
            for i in gpu:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.GPU_name))  # Заполняем название
                self.component_id_dict[rowPosition] = i.GPU_id
        elif index == 3:
            ram = self.session.query(RAM).all()
            for i in ram:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.RAM_name))  # Заполняем название
                self.component_id_dict[rowPosition] = i.RAM_id
        elif index == 4:
            cooler = self.session.query(Cooler).all()
            for i in cooler:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.cooler_name))  # Заполняем название
                self.component_id_dict[rowPosition] = i.cooler_id

    def check_compability(self):
        # if self.index == 0:
        #     dialog = Dialog("Выберите тип комплектующего!")
        #     dialog.exec_()
        #     return
        # if self.tableWidget.currentRow() < 0:
        #     dialog = Dialog("Выберите, что продавать!")
        #     dialog.exec_()
        #     return
        # if len(self.line_edit_price.text()) == 0:
        #     dialog = Dialog("Укажите цену!")
        #     dialog.exec_()
        #     return
        # if not self.line_edit_price.text().isdigit():
        #     dialog = Dialog("Введены непозволительные данные!")
        #     dialog.exec_()
        #     return
        #
        # dialog = Dialog("Подтвердите создание лота!")
        # ret_value = dialog.exec_()
        # if ret_value == QDialog.Accepted:
        #     component = self.comboBox.currentIndex()
        #     if component == 1: # Создание лота CPU
        #         new_lot = Lot(seller_id=self.seller.seller_id,
        #                       price=self.line_edit_price.text(),
        #                       GPU_id=None,
        #                       CPU_id=self.component_id_dict[self.tableWidget.currentRow()],
        #                       MB_id=None,
        #                       RAM_id=None,
        #                       PU_id=None,
        #                       mem_id=None,
        #                       cooler_id=None,
        #                       count=self.spinBox.value())
        #         self.session.add(new_lot)
        #         self.session.commit()
        #     elif component == 2: # Создание лота MB
        #         new_lot = Lot(seller_id=self.seller.seller_id,
        #                      price=self.line_edit_price.text(),
        #                      GPU_id=None,
        #                      CPU_id=None,
        #                      MB_id=self.component_id_dict[self.tableWidget.currentRow()],
        #                      RAM_id=None,
        #                      PU_id=None,
        #                      mem_id=None,
        #                      cooler_id=None,
        #                      count=self.spinBox.value())
        #         self.session.add(new_lot)
        #         self.session.commit()
        #     elif component == 3: # Создание лота GPU
        #         new_lot = Lot(seller_id=self.seller.seller_id,
        #                      price=self.line_edit_price.text(),
        #                      GPU_id=self.component_id_dict[self.tableWidget.currentRow()],
        #                      CPU_id=None,
        #                      MB_id=None,
        #                      RAM_id=None,
        #                      PU_id=None,
        #                      mem_id=None,
        #                      cooler_id=None,
        #                      count=self.spinBox.value())
        #         self.session.add(new_lot)
        #         self.session.commit()
        #     elif component == 4: # Создание лота GPU
        #         new_lot = Lot(seller_id=self.seller.seller_id,
        #                      price=self.line_edit_price.text(),
        #                      GPU_id=None,
        #                      CPU_id=None,
        #                      MB_id=None,
        #                      RAM_id=None,
        #                      PU_id=None,
        #                      mem_id=None,
        #                      cooler_id=self.component_id_dict[self.tableWidget.currentRow()],
        #                      count=self.spinBox.value())
        #         self.session.add(new_lot)
        #         self.session.commit()
        #     elif component == 5: # Создание лота RAM
        #         new_lot = Lot(seller_id=self.seller.seller_id,
        #                      price=self.line_edit_price.text(),
        #                      GPU_id=None,
        #                      CPU_id=None,
        #                      MB_id=None,
        #                      RAM_id=self.component_id_dict[self.tableWidget.currentRow()],
        #                      PU_id=None,
        #                      mem_id=None,
        #                      cooler_id=None,
        #                      count=self.spinBox.value())
        #         self.session.add(new_lot)
        #         self.session.commit()
        #     elif component == 6: # Создание лота RAM
        #         new_lot = Lot(seller_id=self.seller.seller_id,
        #                      price=self.line_edit_price.text(),
        #                      GPU_id=None,
        #                      CPU_id=None,
        #                      MB_id=None,
        #                      RAM_id=None,
        #                      PU_id=None,
        #                      mem_id=self.component_id_dict[self.tableWidget.currentRow()],
        #                      cooler_id=None,
        #                      count=self.spinBox.value())
        #         self.session.add(new_lot)
        #         self.session.commit()
        #     elif component == 7: # Создание лота PU
        #         new_lot = Lot(seller_id=self.seller.seller_id,
        #                      price=self.line_edit_price.text(),
        #                      GPU_id=None,
        #                      CPU_id=None,
        #                      MB_id=None,
        #                      RAM_id=None,
        #                      PU_id=self.component_id_dict[self.tableWidget.currentRow()],
        #                      mem_id=None,
        #                      cooler_id=None,
        #                      count=self.spinBox.value())
        #         self.session.add(new_lot)
        #         self.session.commit()
        #     self.custom_close()
        self.custom_close()

    def custom_close(self):
        self.close()
