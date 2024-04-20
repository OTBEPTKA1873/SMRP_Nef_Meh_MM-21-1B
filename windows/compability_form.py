from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem

from ORM import get_session, CPU, MB, GPU, Cooler, RAM
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
        component = self.componentBox.currentIndex()
        mb = self.session.query(MB).all()
        if component == 1:  # Проверка CPU
            for i in mb:
                if self.session.query(CPU).get(self.component_id_dict[self.componentTable.currentRow()]).socket == i.socket_type:
                    rowPosition = self.mbTable.rowCount()
                    self.mbTable.insertRow(rowPosition)  # Создание строчки
                    self.mbTable.setItem(rowPosition, 0, QTableWidgetItem(i.MB_name))
        elif component == 2:  # Проверка GPU
            for i in mb:
                if self.session.query(GPU).get(self.component_id_dict[self.componentTable.currentRow()]).GPU_type == i.GPU_type:
                    rowPosition = self.mbTable.rowCount()
                    self.mbTable.insertRow(rowPosition)  # Создание строчки
                    self.mbTable.setItem(rowPosition, 0, QTableWidgetItem(i.MB_name))
        elif component == 3:  # Проверка RAM
            for i in mb:
                if self.session.query(RAM).get(self.component_id_dict[self.componentTable.currentRow()]).RAM_type == i.RAM_type:
                    rowPosition = self.mbTable.rowCount()
                    self.mbTable.insertRow(rowPosition)  # Создание строчки
                    self.mbTable.setItem(rowPosition, 0, QTableWidgetItem(i.MB_name))
        elif component == 4:  # Проверка cooler
            for i in mb:
                if self.session.query(Cooler).get(self.component_id_dict[self.componentTable.currentRow()]).socket == i.socket_type:
                    rowPosition = self.mbTable.rowCount()
                    self.mbTable.insertRow(rowPosition)  # Создание строчки
                    self.mbTable.setItem(rowPosition, 0, QTableWidgetItem(i.MB_name))
