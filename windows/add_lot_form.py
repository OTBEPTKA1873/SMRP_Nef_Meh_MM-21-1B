from typing import Iterable, Callable

from PyQt5.QtWidgets import QWidget, QDialog, QTableWidget, QTableWidgetItem

from ORM import get_session, Lot, User, CPU, MB, GPU, Cooler, RAM, Memory, PU
from ui_qt import UiAddLotForm
#from .dialog import Dialog
class LotAdd(QWidget, UiAddLotForm):

    def __init__(self, callbacks: Iterable[Callable]):
        super().__init__()
        self.callbacks = callbacks
        self.setupUi(self)
        self.session = get_session()
        self.push_button_create.clicked.connect(self.create_lot)  # Создание окна
        self.push_button_close.clicked.connect(lambda: self.close()) #Закрытие окна
        self.comboBox.activated.connect(self.activated) # Вызов функции activated

    def activated(self, index):
        self.tableWidget.setRowCount(0)
        if index == 1:
            cpu = self.session.query(CPU).all()
            for i in cpu:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.CPU_name))  # Заполняем строки
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem("Hello"))
        elif index == 2:
            mb = self.session.query(MB).all()
            for i in mb:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.MB_name))  # Заполняем строки
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem("Hello"))
        self.tableWidget.cellDoubleClicked.connect(self.create_lot)

    def create_lot(self):


        self.session.add()
        self.session.commit()

        self.custom_close()


    def custom_close(self):
        for callback in self.callbacks:
            callback()
        self.close()





    # self.comboBox.setItemText(0, _translate("Form", "Процессоры"))
    # self.comboBox.setItemText(1, _translate("Form", "Мат. платы"))
    # self.comboBox.setItemText(2, _translate("Form", "Видеокарты"))
    # self.comboBox.setItemText(3, _translate("Form", "Охлаждение"))
    # self.comboBox.setItemText(4, _translate("Form", "Оперативная память"))
    # self.comboBox.setItemText(5, _translate("Form", "Накопители"))
    # self.comboBox.setItemText(6, _translate("Form", "Блоки питания"))