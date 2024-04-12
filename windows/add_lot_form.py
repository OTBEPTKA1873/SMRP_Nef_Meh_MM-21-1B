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
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(f"{i.ALU} Ядер,  {i.freq} Гц,  {i.socket}, Тепловыделение: {i.TDP} Вт"))
        elif index == 2:
            mb = self.session.query(MB).all()
            for i in mb:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.MB_name))  # Заполняем строки
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(f"{i.form_factor},  {i.socket_type},  {i.RAM_type}x{i.RAM_count},  {i.freq} Гц,  {i.GPU_type}"))
        elif index == 3:
            gpu = self.session.query(GPU).all()
            for i in gpu:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.GPU_name))  # Заполняем строки
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(f"{i.freq} Гц,  {i.ALU} Ядер,  {i.volume} Гб,  {i.GPU_type}"))
        elif index == 4:
            cooler = self.session.query(Cooler).all()
            for i in cooler:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.cooler_name))  # Заполняем строки
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(f"{i.socket},  {i.DH} Вт,  {i.noise} Дб"))
        elif index == 5:
            ram = self.session.query(RAM).all()
            for i in ram:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.RAM_name))  # Заполняем строки
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(f"{i.RAM_type},  {i.volume} Гб,  {i.freq} Гц"))
        elif index == 6:
            mem = self.session.query(Memory).all()
            for i in mem:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.mem_name))  # Заполняем строки
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(f"{i.mem_type},  {i.volume} Гб, скорость: {i.speed} Мб/с"))
        elif index == 7:
            pu = self.session.query(PU).all()
            for i in pu:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)  # Создание строчки
                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(i.PU_name))  # Заполняем строки
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(f"{i.watt} Вт"))
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