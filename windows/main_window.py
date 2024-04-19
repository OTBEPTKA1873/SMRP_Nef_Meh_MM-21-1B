from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from ORM import get_session, Lot, User, CPU
from ui_qt import UiMainWindow
from .dialog import Dialog
from .registration_form import Registration
from .add_lot_form import LotAdd
from .buy_lot_form import LotBuy
from .update_lot_form import LotUpdate
from .receipts_form import Receipts
from .compability_form import Compability


class MainWindow(QMainWindow, UiMainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.create_window = None
        self.session = None
        self.current_row = None
        self.current_user = None

        self.push_button_register.clicked.connect(self.open_register)
        self.push_button_create.clicked.connect(self.open_lot_add)
        self.push_button_buy.clicked.connect(self.open_lot_buy)
        self.tableWidget.cellDoubleClicked.connect(self.open_lot_update)
        self.push_button_receipts.clicked.connect(self.open_receipts)
        self.push_button_sort.clicked.connect(self.compability)
        self.tableWidget.cellClicked.connect(self.table_widget_cell_clicked)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3)

        self.open_register()
        self.update_table()
        # Сортировка
        self.componentBox.activated.connect(self.activated)  # Вызов функции activated
        self.parametrBox.activated.connect(self.parametr)  # Вызов функции activated
        self.valueBox.activated.connect(self.value)  # Вызов функции activated
        self.pushButton.clicked.connect(self.sorting_lot)

    def update_table(self):
        self.session = get_session()
        lots = self.session.query(Lot).where(Lot.count > 0).order_by(Lot.lot_id).all()
        self.tableWidget.setRowCount(0)
        for lot in lots:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setItem(row_position, 0, QTableWidgetItem(str(lot.lot_id)))
            self.tableWidget.setItem(row_position, 1, QTableWidgetItem(f"{lot.seller.user.last_name} {lot.seller.user.first_name} {lot.seller.user.patronymic if lot.seller.user.patronymic else ''}"))
            self.tableWidget.setItem(row_position, 2, QTableWidgetItem(lot.component_name()))
            self.tableWidget.setItem(row_position, 3, QTableWidgetItem(str(lot.price)))
            self.tableWidget.setItem(row_position, 4, QTableWidgetItem(str(lot.count)))
        self.session.close()

    def table_widget_cell_clicked(self, row, column):
        self.current_row = row

    def update_user(self, user):
        self.current_user = user

    def open_register(self):
        self.create_window = Registration([self.update_user])
        self.create_window.show()

    def open_lot_buy(self):
        if self.current_user is None:
            self.open_register()
            self.current_row = None
            return
        if self.current_row is None:
            dialog = Dialog("Выберите лот!")
            dialog.exec_()
            return
        lot_id = int(self.tableWidget.item(self.current_row, 0).text())
        lot = self.session.query(Lot).get(lot_id)
        if self.current_user.user_id == lot.seller.user.user_id:
            dialog = Dialog("Это Ваш лот!")
            dialog.exec_()
            self.current_row = None
            return
        self.current_row = None
        self.create_window = LotBuy(lot, self.current_user, [self.update_table])
        self.create_window.show()

    def open_lot_update(self, row, column):
        lot_id = int(self.tableWidget.item(row, 0).text())
        lot = self.session.query(Lot).get(lot_id)
        self.create_window = LotUpdate(lot, self.current_user, [self.update_table])
        self.create_window.show()

    def open_lot_add(self):
        if self.current_user is None:
            self.open_register()
            return
        self.create_window = LotAdd(self.current_user, [self.update_table])
        self.create_window.show()

    def open_receipts(self):
        if self.current_user is None:
            self.open_register()
            return
        self.create_window = Receipts(self.current_user)
        self.create_window.show()

    def compability(self):
        self.create_window = Compability()
        self.create_window.show()

    def value(self, index):
        self.index = index
        if index == 0 and self.parametrBox.currentIndex() == 0:
            dialog = Dialog("Предварительно выберите характеристику!")
            dialog.exec_()
            return

    def activated(self, index): # Заполнение comboBox с информацией о видах характеристик
        if index == 0 and self.componentBox.currentIndex() == 0:
            dialog = Dialog("Предварительно выберите тип комплектующего!")
            dialog.exec_()
            return
        self.index = index
        self.parametrBox.clear()
        self.parametrBox.addItems(list("Характеристика".split("*"))) # Кто моему коду ломает ноги?
        if index == 1: # CPU
            self.parametrBox.addItems(list("Число ядер * Частота (Гц) * Сокет * Тепловыделение (Вт)".split(" * ")))
        elif index == 2: # MB
            self.parametrBox.addItems(list("Форм-фактор * Тип оперативной памяти * Частота (Гц) * Тип видеокарты".split(" * ")))
        elif index == 3: # GPU
            self.parametrBox.addItems(list("Частота (Гц) * Число ядер * Объем памяти (Гб) * Тип видеокарты".split(" * ")))
        elif index == 4: # cooler
            self.parametrBox.addItems(list("Сокет * Рассеивание тепла * Шум (Дб)".split(" * ")))
        elif index == 5: # RAM
            self.parametrBox.addItems(list("Тип оперативной памяти * Объем памяти (Гб) * Частота (Гц)".split(" * ")))
        elif index == 6: # It`s wednesday my dudes (memory)
            self.parametrBox.addItems(list("Тип накопителя * Объем памяти (Гб) * Скорость (Мб/с)".split(" * ")))
        elif index == 7: # PU
            self.parametrBox.addItems(list("Мощность".split(" ")))

    def parametr(self, index):
        self.index = index
        if index == 0 and self.componentBox.currentIndex() == 0:
            dialog = Dialog("Предварительно выберите тип комплектующего!")
            dialog.exec_()
            return
        self.valueBox.clear()
        self.valueBox.addItems(list("Значение".split("*")))  # Кто моему коду ломает ноги?
        if self.componentBox.currentIndex() == 1:  # CPU
            if index == 1:  # Число ядер
                self.valueBox.addItems(list("<6 * 6-8 * 8-10 * 10-12 * >12".split(" * ")))
            elif index == 2:  # Частота
                self.valueBox.addItems(
                    list("<2000 Гц * 2000-2500 Гц * 2500-3000 Гц * 3000-3500 Гц * >3500 Гц".split(" * ")))
            elif index == 3:  # Сокет
                self.valueBox.addItems(list("LGA сокеты * AM сокеты * Другие сокеты".split(" * ")))
            elif index == 4:
                self.valueBox.addItems(list(">70 Вт * 70-80 Вт * 80-90 Вт * 90-100 Вт * <100 Вт".split(" * ")))
        elif self.componentBox.currentIndex() == 2:  # MB
                if index == 1:  # Форм-фактор
                    self.valueBox.addItems(list("mini-ITX * micro-ATX * ATX * EATX".split(" * ")))
                elif index == 2:  # Тип оперативной памяти
                    self.valueBox.addItems(list("DDR * DDR2 * DDR3 * DDR4 * DDR5".split(" * ")))
                elif index == 3:  # Частота
                    self.valueBox.addItems(
                        list("<2000 Гц * 2000-2500 Гц * 2500-3000 Гц * 3000-3500 Гц * >3500 Гц".split(" * ")))
                elif index == 4: # Тип видеокарты
                    self.valueBox.addItems(list("PCI-E 2.0 * PCI-E 3.0 * PCI-E 4.0".split(" * ")))
        elif self.componentBox.currentIndex() == 3:  # GPU
                if index == 1:  # Частота
                    self.valueBox.addItems(
                        list("<2000 Гц * 2000-2500 Гц * 2500-3000 Гц * 3000-3500 Гц * >3500 Гц".split(" * ")))
                elif index == 2:  # Число ядер
                    self.valueBox.addItems(list("<6 * 6-8 * 8-10 * 10-12 * >12".split(" * ")))
                elif index == 3:  # Объем памяти
                    self.valueBox.addItems(
                        list("0-4 Гб * 4-8 Гб * 8-16 Гб * >16 Гб".split(" * ")))
                elif index == 4: # Тип видеокарты
                    self.valueBox.addItems(list("PCI-E 2.0 * PCI-E 3.0 * PCI-E 4.0".split(" * ")))
        elif self.componentBox.currentIndex() == 4:  # cooler
                if index == 1:  # Сокет
                    self.valueBox.addItems(
                        list("LGA сокеты * AM сокеты * Другие сокеты".split(" * ")))
                elif index == 2:  # Рассеивание тепла
                    self.valueBox.addItems(list("<40 Вт * 40-60 Вт * 60-80 Вт * >80 Вт".split(" * ")))
                elif index == 3:  # Шум
                    self.valueBox.addItems(list("<20 Дб * 20-30 Дб * 30-40 Дб * >40 Дб".split(" * ")))
        elif self.componentBox.currentIndex() == 5:  # RAM
                if index == 1:  # Тип оперативной памяти
                    self.valueBox.addItems(list("DDR * DDR2 * DDR3 * DDR4 * DDR5".split(" * ")))
                elif index == 2:  # Объем памяти
                    self.valueBox.addItems(list("<8 Гб * 8-16 Гб * 16-32 Гб * >32 Гб".split(" * ")))
                elif index == 3:  # Частота
                    self.valueBox.addItems(
                    list("<2000 Гц * 2000-2500 Гц * 2500-3000 Гц * 3000-3500 Гц * >3500 Гц".split(" * ")))
        elif self.componentBox.currentIndex() == 6:  # memory
                if index == 1:  # Тип накопителя
                    self.valueBox.addItems(list("HDD 3.5'' * SSD 2.5'' * SSD M.2".split(" * ")))
                elif index == 2:  # Объем памяти
                    self.valueBox.addItems(list("<250 Гб * 250-500 Гб * 500-1000 Гб * >1000 Гб ".split(" * ")))
                elif index == 3:  # Скорость
                    self.valueBox.addItems(list("<250 Мб/с * 250-500 Мб/с * 500-1000 Мб/с * >1000 Мб/с".split(" * ")))
        elif self.componentBox.currentIndex() == 7:  # PU
                if index == 1:  # Мощность
                    self.valueBox.addItems(list("<250 Вт * 250-500 Вт * 500-750 Вт * >750 Вт".split(" * ")))

    def sorting_lot(self):
        if self.componentBox.currentIndex() == 0 or self.parametrBox.currentIndex() == 0 or self.parametrBox.currentIndex() == 0:
            dialog = Dialog("Выберите все параметры!")
            dialog.exec_()
            return
        self.tableWidget.setRowCount(0) # Чистим таблицу от не нужного
        lots = self.session.query(Lot).where(Lot.count > 0).all()  # Проверяем лоты на сущ.
        # Уровень комплектующего
        if self.componentBox.currentIndex() == 1: # CPU
            # Уровень характеристик
            if self.parametrBox.currentIndex() == 1: # CPU___ALU
                if self.valueBox.currentIndex() == 1: # ALU <6
                    cpus = self.session.query(CPU).where(CPU.ALU <= 6).all()
                    for lot in lots:
                        for cpu in cpus:
                            if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2: # ALU 6-8
                    cpus = self.session.query(CPU).where(CPU.ALU >= 6).where(CPU.ALU <= 8).all()
                    for lot in lots:
                        for cpu in cpus:
                            if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3: # ALU 8-10
                    cpus = self.session.query(CPU).where(CPU.ALU >= 8).where(CPU.ALU <= 10).all()
                    for lot in lots:
                        for cpu in cpus:
                            if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4: # ALU 10-12
                    cpus = self.session.query(CPU).where(CPU.ALU >= 10).where(CPU.ALU <= 12).all()
                    for lot in lots:
                        for cpu in cpus:
                            if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 5: # ALU >12
                    cpus = self.session.query(CPU).where(CPU.ALU >= 12).all()
                    for lot in lots:
                        for cpu in cpus:
                            if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
                                self.sort_lot(lot)
            if self.parametrBox.currentIndex() == 2: # CPU___freq
                if self.valueBox.currentIndex() == 1: # freq <2000
                    cpus = self.session.query(CPU).where(CPU.freq <= 2000).all()
                    for lot in lots:
                        for cpu in cpus:
                            if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2: # freq 2000-2500
                    cpus = self.session.query(CPU).where(CPU.freq >= 2000).where(CPU.freq <= 2500).all()
                    for lot in lots:
                        for cpu in cpus:
                            if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3: # freq 2500-3000
                    cpus = self.session.query(CPU).where(CPU.freq >= 2500).where(CPU.freq <= 3000).all()
                    for lot in lots:
                        for cpu in cpus:
                            if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4: # freq 3000-3500
                    cpus = self.session.query(CPU).where(CPU.freq >= 3000).where(CPU.freq <= 3500).all()
                    for lot in lots:
                        for cpu in cpus:
                            if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 5: # freq >3500
                    cpus = self.session.query(CPU).where(CPU.freq >= 3500).all()
                    for lot in lots:
                        for cpu in cpus:
                            if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
                                self.sort_lot(lot)
            # if self.parametrBox.currentIndex() == 3: # CPU___Сокет
            #     if self.valueBox.currentIndex() == 1: # freq <2000
            #         cpus = self.session.query(CPU).where(CPU.freq <= 2000).all()
            #         for lot in lots:
            #             for cpu in cpus:
            #                 if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
            #                     self.sort_lot(lot)
            #     elif self.valueBox.currentIndex() == 2: # freq 2000-2500
            #         cpus = self.session.query(CPU).where(CPU.freq >= 2000).where(CPU.freq <= 2500).all()
            #         for lot in lots:
            #             for cpu in cpus:
            #                 if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
            #                     self.sort_lot(lot)
            #     elif self.valueBox.currentIndex() == 3: # freq 2500-3000
            #         cpus = self.session.query(CPU).where(CPU.freq >= 2500).where(CPU.freq <= 3000).all()
            #         for lot in lots:
            #             for cpu in cpus:
            #                 if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
            #                     self.sort_lot(lot)
            #     elif self.valueBox.currentIndex() == 4: # freq 3000-3500
            #         cpus = self.session.query(CPU).where(CPU.freq >= 3000).where(CPU.freq <= 3500).all()
            #         for lot in lots:
            #             for cpu in cpus:
            #                 if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
            #                     self.sort_lot(lot)
            #     elif self.valueBox.currentIndex() == 5: # freq >3500
            #         cpus = self.session.query(CPU).where(CPU.freq >= 3500).all()
            #         for lot in lots:
            #             for cpu in cpus:
            #                 if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
            #                     self.sort_lot(lot)

    def sort_lot(self, lot: Lot):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setItem(row_position, 0, QTableWidgetItem(str(lot.lot_id)))
        self.tableWidget.setItem(row_position, 1, QTableWidgetItem(
            f"{lot.seller.user.last_name} {lot.seller.user.first_name} {lot.seller.user.patronymic if lot.seller.user.patronymic else ''}"))
        self.tableWidget.setItem(row_position, 2, QTableWidgetItem(lot.component_name()))
        self.tableWidget.setItem(row_position, 3, QTableWidgetItem(str(lot.price)))
        self.tableWidget.setItem(row_position, 4, QTableWidgetItem(str(lot.count)))