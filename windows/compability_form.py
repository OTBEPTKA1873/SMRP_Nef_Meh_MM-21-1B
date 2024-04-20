from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem

from ORM import get_session, CPU, GPU, Cooler, RAM, MB, CPU_MB, GPU_MB, Cooler_MB, RAM_MB
from ui_qt import UiCompability
from .dialog import Dialog


class Compability(QWidget, UiCompability):

    def __init__(self):
        super().__init__()

        self.component_id_dict = {}  # Создаем словарь для id
        self.setupUi(self)
        self.session = get_session()
        self.index = 0

        self.componentBox.activated.connect(self.activated) # Вызов функции activated
        self.pushButton.clicked.connect(self.check_compability)
        self.componentTable.horizontalHeader().setSectionResizeMode(3)

    def activated(self, index):
        self.index = index
        self.componentTable.setRowCount(0)
        self.mbTable.setRowCount(0)
        self.component_id_dict.clear()
        self.component_id_dict.clear()
        if index == 1:
            cpu = self.session.query(CPU).all()
            for i in cpu:
                rowPosition = self.componentTable.rowCount()
                self.componentTable.insertRow(rowPosition)  # Создание строчки
                self.componentTable.setItem(rowPosition, 0, QTableWidgetItem(i.CPU_name))
                self.component_id_dict[rowPosition] = i.CPU_id
        elif index == 2:
            gpu = self.session.query(GPU).all()
            for i in gpu:
                rowPosition = self.componentTable.rowCount()
                self.componentTable.insertRow(rowPosition)  # Создание строчки
                self.componentTable.setItem(rowPosition, 0, QTableWidgetItem(i.GPU_name))
                self.component_id_dict[rowPosition] = i.GPU_id
        elif index == 3:
            ram = self.session.query(RAM).all()
            for i in ram:
                rowPosition = self.componentTable.rowCount()
                self.componentTable.insertRow(rowPosition)  # Создание строчки
                self.componentTable.setItem(rowPosition, 0, QTableWidgetItem(i.RAM_name))
                self.component_id_dict[rowPosition] = i.RAM_id
        elif index == 4:
            cooler = self.session.query(Cooler).all()
            for i in cooler:
                rowPosition = self.componentTable.rowCount()
                self.componentTable.insertRow(rowPosition)  # Создание строчки
                self.componentTable.setItem(rowPosition, 0, QTableWidgetItem(i.cooler_name))
                self.component_id_dict[rowPosition] = i.cooler_id

    def check_compability(self):
        self.mbTable.setRowCount(0)
        if self.componentTable.currentRow() < 0:
            dialog = Dialog("Выберите к чему подбирать материнскую плату!")
            dialog.exec_()
            return
        if self.componentBox.currentIndex() == 1:  # Проверка CPU
            cpu_mbs = self.session.query(CPU_MB).where(CPU_MB.CPU_id == self.component_id_dict[self.componentTable.currentRow()])
            for i in cpu_mbs:
                mbs = self.session.query(MB.MB_name).where(MB.MB_id == i.MB_id).all()
                for j in mbs:
                    rowPosition = self.mbTable.rowCount()
                    self.mbTable.insertRow(rowPosition)  # Создание строчки
                    self.mbTable.setItem(rowPosition, 0, QTableWidgetItem(j[0]))
        elif self.componentBox.currentIndex() == 2:  # Проверка GPU
            gpu_mbs = self.session.query(GPU_MB).where(GPU_MB.GPU_id == self.component_id_dict[self.componentTable.currentRow()])
            for i in gpu_mbs:
                mbs = self.session.query(MB.MB_name).where(MB.MB_id == i.MB_id).all()
                for j in mbs:
                    rowPosition = self.mbTable.rowCount()
                    self.mbTable.insertRow(rowPosition)  # Создание строчки
                    self.mbTable.setItem(rowPosition, 0, QTableWidgetItem(j[0]))
        elif self.componentBox.currentIndex() == 3:  # Проверка RAM
            ram_mbs = self.session.query(RAM_MB).where(RAM_MB.RAM_id == self.component_id_dict[self.componentTable.currentRow()])
            for i in ram_mbs:
                rams = self.session.query(MB.MB_name).where(MB.MB_id == i.MB_id).all()
                for j in rams:
                    rowPosition = self.mbTable.rowCount()
                    self.mbTable.insertRow(rowPosition)  # Создание строчки
                    self.mbTable.setItem(rowPosition, 0, QTableWidgetItem(j[0]))
        elif self.componentBox.currentIndex() == 4:  # Проверка Cooler
            cooler_mbs = self.session.query(Cooler_MB).where(Cooler_MB.cooler_id == self.component_id_dict[self.componentTable.currentRow()])
            for i in cooler_mbs:
                coolers = self.session.query(MB.MB_name).where(MB.MB_id == i.MB_id).all()
                for j in coolers:
                    rowPosition = self.mbTable.rowCount()
                    self.mbTable.insertRow(rowPosition)  # Создание строчки
                    self.mbTable.setItem(rowPosition, 0, QTableWidgetItem(j[0]))