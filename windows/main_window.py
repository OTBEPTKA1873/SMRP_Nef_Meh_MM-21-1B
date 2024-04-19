from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from ORM import get_session, Lot, User, CPU, MB, GPU, Cooler, RAM, Memory, PU
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
        if self.componentBox.currentIndex() == 0:
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
                self.valueBox.addItems(list(">70 Вт * 70-90 Вт * 90-110 Вт * <110 Вт".split(" * ")))
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
                    self.valueBox.addItems(list("<2000 * 2000-3000 * 3000-4000 * 4000-6000 * >6000".split(" * ")))
                elif index == 3:  # Объем памяти
                    self.valueBox.addItems(
                        list("<4 Гб * 4-8 Гб * 8-16 Гб * >16 Гб".split(" * ")))
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
        if self.componentBox.currentIndex() == 0 or self.parametrBox.currentIndex() == 0 or self.valueBox.currentIndex() == 0:
            dialog = Dialog("Выберите все параметры!")
            dialog.exec_()
            return
        self.tableWidget.setRowCount(0) # Чистим таблицу от не нужного
        lots = self.session.query(Lot).where(Lot.count > 0).all()  # Проверяем лоты на сущ.
        # Уровень комплектующего
        if self.componentBox.currentIndex() == 1: # CPU
            # Уровень характеристик
            if self.parametrBox.currentIndex() == 1: # CPU___ALU
                # Уровень Значений
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
            elif self.parametrBox.currentIndex() == 2: # CPU___freq
                # Уровень Значений
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
            elif self.parametrBox.currentIndex() == 3: # CPU___Сокет
                # Уровень Значений
                cpus = self.session.query(CPU).all()
                if self.valueBox.currentIndex() == 1: # LGA
                    for lot in lots:
                        for cpu in cpus:
                            if "LGA" in cpu.socket:
                                if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2: # AM
                    for lot in lots:
                        for cpu in cpus:
                            if "AM" in cpu.socket:
                                if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
                                    self.sort_lot(lot)
                else: # Другие
                    for lot in lots:
                        for cpu in cpus:
                            if not("AM" in cpu.socket or "LGA" in cpu.socket):
                                if lot.CPU_id == cpu.CPU_id: # Проверка на то, что в лоте именно CPU
                                    self.sort_lot(lot)
            elif self.parametrBox.currentIndex() == 4: # CPU___TDP
                # Уровень Значений
                if self.valueBox.currentIndex() == 1:  # TDP <70
                    cpus = self.session.query(CPU).where(CPU.TDP <= 70).all()
                    for lot in lots:
                        for cpu in cpus:
                            if lot.CPU_id == cpu.CPU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2:  # TDP 70-110
                    cpus = self.session.query(CPU).where(CPU.TDP >= 70).where(CPU.TDP <= 90).all()
                    for lot in lots:
                        for cpu in cpus:
                            if lot.CPU_id == cpu.CPU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3:  # TDP 90-110
                    cpus = self.session.query(CPU).where(CPU.TDP >= 90).where(CPU.TDP <= 110).all()
                    for lot in lots:
                        for cpu in cpus:
                            if lot.CPU_id == cpu.CPU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4:  # TDP >110
                    cpus = self.session.query(CPU).where(CPU.TDP >= 110).all()
                    for lot in lots:
                        for cpu in cpus:
                            if lot.CPU_id == cpu.CPU_id:
                                self.sort_lot(lot)
        elif self.componentBox.currentIndex() == 2: # MB
            # Уровень характеристик
            if self.parametrBox.currentIndex() == 1: # MB___form-factor
                # Уровень Значений
                mbs = self.session.query(MB).all()
                if self.valueBox.currentIndex() == 1: # Mini-ITX
                    for lot in lots:
                        for mb in mbs:
                            if "Mini-ITX" in mb.form_factor:
                                if lot.MB_id == mb.MB_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2: # Micro-ATX
                    for lot in lots:
                        for mb in mbs:
                            if "Micro-ATX" in mb.form_factor:
                                if lot.MB_id == mb.MB_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3: # ATX
                    for lot in lots:
                        for mb in mbs:
                            if "ATX" in mb.form_factor:
                                if lot.MB_id == mb.MB_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4: # EATX
                    for lot in lots:
                        for mb in mbs:
                            if "EATX" in mb.form_factor:
                                if lot.MB_id == mb.MB_id:
                                    self.sort_lot(lot)
            elif self.parametrBox.currentIndex() == 2: # MB___RAM
                # Уровень Значений
                mbs = self.session.query(MB).all()
                if self.valueBox.currentIndex() == 1: # DDR
                    for lot in lots:
                        for mb in mbs:
                            if "DDR" == mb.RAM_type:
                                if lot.MB_id == mb.MB_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2: # DDR2
                    for lot in lots:
                        for mb in mbs:
                            if "DDR2" == mb.RAM_type:
                                if lot.MB_id == mb.MB_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3: # DDR3
                    for lot in lots:
                        for mb in mbs:
                            if "DDR3" == mb.RAM_type:
                                if lot.MB_id == mb.MB_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4: # DDR4
                    for lot in lots:
                        for mb in mbs:
                            if "DDR4" == mb.RAM_type:
                                if lot.MB_id == mb.MB_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 5: # DDR5
                    for lot in lots:
                        for mb in mbs:
                            if "DDR5" == mb.RAM_type:
                                if lot.MB_id == mb.MB_id:
                                    self.sort_lot(lot)
            elif self.parametrBox.currentIndex() == 3: # MB___freq
                # Уровень Значений
                if self.valueBox.currentIndex() == 1: # freq <2000
                    mbs = self.session.query(MB).where(MB.freq <= 2000).all()
                    for lot in lots:
                        for mb in mbs:
                            if lot.MB_id == mb.MB_id: # Проверка на то, что в лоте именно CPU
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2: # freq 2000-2500
                    mbs = self.session.query(MB).where(MB.freq >= 2000).where(MB.freq <= 2500).all()
                    for lot in lots:
                        for mb in mbs:
                            if lot.MB_id == mb.MB_id: # Проверка на то, что в лоте именно CPU
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3: # freq 2500-3000
                    mbs = self.session.query(MB).where(MB.freq >= 2500).where(MB.freq <= 3000).all()
                    for lot in lots:
                        for mb in mbs:
                            if lot.MB_id == mb.MB_id: # Проверка на то, что в лоте именно CPU
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4: # freq 3000-3500
                    mbs = self.session.query(MB).where(MB.freq >= 3000).where(MB.freq <= 3500).all()
                    for lot in lots:
                        for mb in mbs:
                            if lot.MB_id == mb.MB_id: # Проверка на то, что в лоте именно CPU
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 5: # freq >3500
                    mbs = self.session.query(MB).where(MB.freq >= 3500).all()
                    for lot in lots:
                        for mb in mbs:
                            if lot.MB_id == mb.MB_id: # Проверка на то, что в лоте именно CPU
                                self.sort_lot(lot)
            elif self.parametrBox.currentIndex() == 4: # MB___GPU
                # Уровень Значений
                mbs = self.session.query(MB).all()
                if self.valueBox.currentIndex() == 1: # PCI-E 2.0
                    for lot in lots:
                        for mb in mbs:
                            if "PCI-E 2.0" == mb.GPU_type:
                                if lot.MB_id == mb.MB_id: # Проверка на то, что в лоте именно CPU
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2: # PCI-E 3.0
                    for lot in lots:
                        for mb in mbs:
                            if "PCI-E 3.0" == mb.GPU_type:
                                if lot.MB_id == mb.MB_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3: # PCI-E 4.0
                    for lot in lots:
                        for mb in mbs:
                            if "PCI-E 4.0" == mb.GPU_type:
                                if lot.MB_id == mb.MB_id:
                                    self.sort_lot(lot)
        elif self.componentBox.currentIndex() == 3: # GPU
            # Уровень характеристик
            if self.parametrBox.currentIndex() == 1:  # GPU___freq
                # Уровень Значений
                if self.valueBox.currentIndex() == 1:  # freq <2000
                    gpus = self.session.query(GPU).where(GPU.freq <= 2000).all()
                    for lot in lots:
                        for gpu in gpus:
                            if lot.GPU_id == gpu.GPU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2:  # freq 2000-2500
                    gpus = self.session.query(GPU).where(GPU.freq >= 2000).where(GPU.freq <= 2500).all()
                    for lot in lots:
                        for gpu in gpus:
                            if lot.GPU_id == gpu.GPU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3:  # freq 2500-3000
                    gpus = self.session.query(GPU).where(GPU.freq >= 2500).where(GPU.freq <= 3000).all()
                    for lot in lots:
                        for gpu in gpus:
                            if lot.GPU_id == gpu.GPU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4:  # freq 3000-3500
                    gpus = self.session.query(GPU).where(GPU.freq >= 3000).where(GPU.freq <= 3500).all()
                    for lot in lots:
                        for gpu in gpus:
                            if lot.GPU_id == gpu.GPU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 5:  # freq >3500
                    gpus = self.session.query(GPU).where(GPU.freq >= 3500).all()
                    for lot in lots:
                        for gpu in gpus:
                            if lot.GPU_id == gpu.GPU_id:
                                self.sort_lot(lot)
            elif self.parametrBox.currentIndex() == 2:  # GPU___ALU
                # Уровень Значений
                if self.valueBox.currentIndex() == 1:  # ALU <2000
                    gpus = self.session.query(GPU).where(GPU.ALU <= 2000).all()
                    for lot in lots:
                        for gpu in gpus:
                            if lot.GPU_id == gpu.GPU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2:  # ALU 2000-3000
                    gpus = self.session.query(GPU).where(GPU.ALU >= 2000).where(GPU.ALU <= 3000).all()
                    for lot in lots:
                        for gpu in gpus:
                            if lot.GPU_id == gpu.GPU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3:  # ALU 3000-4000
                    gpus = self.session.query(GPU).where(GPU.ALU >= 3000).where(GPU.ALU <= 4000).all()
                    for lot in lots:
                        for gpu in gpus:
                            if lot.GPU_id == gpu.GPU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4:  # ALU 4000-6000
                    gpus = self.session.query(GPU).where(GPU.ALU >= 4000).where(GPU.ALU <= 6000).all()
                    for lot in lots:
                        for gpu in gpus:
                            if lot.GPU_id == gpu.GPU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 5:  # ALU >6000
                    gpus = self.session.query(GPU).where(GPU.ALU >=6000).all()
                    for lot in lots:
                        for gpu in gpus:
                            if lot.GPU_id == gpu.GPU_id:
                                self.sort_lot(lot)
            elif self.parametrBox.currentIndex() == 3:  # GPU___Volume
                # Уровень Значений
                if self.valueBox.currentIndex() == 1:  # volume <4
                    gpus = self.session.query(GPU).where(GPU.volume <= 4).all()
                    for lot in lots:
                        for gpu in gpus:
                            if lot.GPU_id == gpu.GPU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2:  # volume 4-8
                    gpus = self.session.query(GPU).where(GPU.volume >= 4).where(GPU.volume <= 8).all()
                    for lot in lots:
                        for gpu in gpus:
                            if lot.GPU_id == gpu.GPU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3:  # volume 8-16
                    gpus = self.session.query(GPU).where(GPU.volume >= 8).where(GPU.volume <= 16).all()
                    for lot in lots:
                        for gpu in gpus:
                            if lot.GPU_id == gpu.GPU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4:  # volume >16
                    gpus = self.session.query(GPU).where(GPU.volume >=16).all()
                    for lot in lots:
                        for gpu in gpus:
                            if lot.GPU_id == gpu.GPU_id:
                                self.sort_lot(lot)
            elif self.parametrBox.currentIndex() == 4:  # GPU___GPU-type
                # Уровень Значений
                gpus = self.session.query(GPU).all()
                if self.valueBox.currentIndex() == 1:  # PCI-E 2.0
                    for lot in lots:
                        for gpu in gpus:
                            if "PCI-E 2.0" == gpu.GPU_type:
                                if lot.GPU_id == gpu.GPU_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2:  # PCI-E 3.0
                    for lot in lots:
                        for gpu in gpus:
                            if "PCI-E 3.0" == gpu.GPU_type:
                                if lot.GPU_id == gpu.GPU_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3:  # PCI-E 4.0
                    for lot in lots:
                        for gpu in gpus:
                            if "PCI-E 4.0" == gpu.GPU_type:
                                if lot.GPU_id == gpu.GPU_id:
                                    self.sort_lot(lot)
        elif self.componentBox.currentIndex() == 4: # Cooler
            # Уровень характеристик
            if self.parametrBox.currentIndex() == 1:  # Cooler___socket
                # Уровень Значений
                coolers = self.session.query(Cooler).all()
                if self.valueBox.currentIndex() == 1:  # LGA
                    for lot in lots:
                        for cooler in coolers:
                            if "LGA" in cooler.socket:
                                if lot.cooler_id == cooler.cooler_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2:  # AM
                    for lot in lots:
                        for cooler in coolers:
                            if "AM" in cooler.socket:
                                if lot.cooler_id == cooler.cooler_id:
                                    self.sort_lot(lot)
                else:  # Другие
                    for lot in lots:
                        for cooler in coolers:
                            if not("LGA" in cooler.socket or "AM" in cooler.socket):
                                if lot.cooler_id == cooler.cooler_id:
                                    self.sort_lot(lot)
            elif self.parametrBox.currentIndex() == 2:  # Cooler___DH
                # Уровень Значений
                if self.valueBox.currentIndex() == 1:  # DH <40
                    coolers = self.session.query(Cooler).where(Cooler.DH <= 40).all()
                    for lot in lots:
                        for cooler in coolers:
                            if lot.cooler_id == cooler.cooler_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2:  # DH 40-60
                    coolers = self.session.query(Cooler).where(Cooler.DH >= 40).where(Cooler.DH <= 60).all()
                    for lot in lots:
                        for cooler in coolers:
                            if lot.cooler_id == cooler.cooler_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3:  # DH 60-80
                    coolers = self.session.query(Cooler).where(Cooler.DH >= 60).where(Cooler.DH <= 80).all()
                    for lot in lots:
                        for cooler in coolers:
                            if lot.cooler_id == cooler.cooler_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4:  # DH >80
                    coolers = self.session.query(Cooler).where(Cooler.DH >= 80).all()
                    for lot in lots:
                        for cooler in coolers:
                            if lot.cooler_id == cooler.cooler_id:
                                self.sort_lot(lot)
            elif self.parametrBox.currentIndex() == 3:  # Cooler___noise
                # Уровень Значений
                if self.valueBox.currentIndex() == 1:  # DH <20
                    coolers = self.session.query(Cooler).where(Cooler.noise <= 20).all()
                    for lot in lots:
                        for cooler in coolers:
                            if lot.cooler_id == cooler.cooler_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2:  # DH 20-30
                    coolers = self.session.query(Cooler).where(Cooler.noise >= 20).where(Cooler.noise <= 30).all()
                    for lot in lots:
                        for cooler in coolers:
                            if lot.cooler_id == cooler.cooler_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3:  # DH 30-40
                    coolers = self.session.query(Cooler).where(Cooler.noise >= 30).where(Cooler.noise <= 40).all()
                    for lot in lots:
                        for cooler in coolers:
                            if lot.cooler_id == cooler.cooler_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4:  # DH >40
                    coolers = self.session.query(Cooler).where(Cooler.noise >= 40).all()
                    for lot in lots:
                        for cooler in coolers:
                            if lot.cooler_id == cooler.cooler_id:
                                self.sort_lot(lot)
        elif self.componentBox.currentIndex() == 5: # RAM
            # Уровень характеристик
            if self.parametrBox.currentIndex() == 1:  # RAM___RAM-type
                # Уровень Значений
                rams = self.session.query(RAM).all()
                if self.valueBox.currentIndex() == 1:  # DDR
                    for lot in lots:
                        for ram in rams:
                            if "DDR" == ram.RAM_type:
                                if lot.RAM_id == ram.RAM_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2:  # DDR2
                    for lot in lots:
                        for ram in rams:
                            if "DDR2" == ram.RAM_type:
                                if lot.RAM_id == ram.RAM_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3:  # DDR3
                    for lot in lots:
                        for ram in rams:
                            if "DDR3" == ram.RAM_type:
                                if lot.RAM_id == ram.RAM_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4:  # DDR4
                    for lot in lots:
                        for ram in rams:
                            if "DDR4" == ram.RAM_type:
                                if lot.RAM_id == ram.RAM_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 5:  # DDR5
                    for lot in lots:
                        for ram in rams:
                            if "DDR5" == ram.RAM_type:
                                if lot.RAM_id == ram.RAM_id:
                                    self.sort_lot(lot)
            elif self.parametrBox.currentIndex() == 2:  # RAM___Volume
                # Уровень Значений
                if self.valueBox.currentIndex() == 1:  # Volume <8
                    rams = self.session.query(RAM).where(RAM.volume <= 8).all()
                    for lot in lots:
                        for ram in rams:
                            if lot.RAM_id == ram.RAM_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2:  # Volume 8-16
                    rams = self.session.query(RAM).where(RAM.volume >= 8).where(RAM.volume <= 16).all()
                    for lot in lots:
                        for ram in rams:
                            if lot.RAM_id == ram.RAM_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3:  # Volume 16-32
                    rams = self.session.query(RAM).where(RAM.volume >= 16).where(RAM.volume <= 32).all()
                    for lot in lots:
                        for ram in rams:
                            if lot.RAM_id == ram.RAM_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4:  # Volume >32
                    rams = self.session.query(RAM).where(RAM.volume >= 32).all()
                    for lot in lots:
                        for ram in rams:
                            if lot.RAM_id == ram.RAM_id:
                                    self.sort_lot(lot)
            elif self.parametrBox.currentIndex() == 3:  # RAM___freq
                # Уровень Значений
                if self.valueBox.currentIndex() == 1:  # freq <2000
                    rams = self.session.query(RAM).where(RAM.freq <= 2000).all()
                    for lot in lots:
                        for ram in rams:
                            if lot.RAM_id == ram.RAM_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2:  # freq 2000-2500
                    rams = self.session.query(RAM).where(RAM.freq >= 2000).where(RAM.freq <= 2500).all()
                    for lot in lots:
                        for ram in rams:
                            if lot.RAM_id == ram.RAM_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3:  # freq 2500-3000
                    rams = self.session.query(RAM).where(RAM.freq >= 2500).where(RAM.freq <= 3000).all()
                    for lot in lots:
                        for ram in rams:
                            if lot.RAM_id == ram.RAM_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4:  # freq 3000-3500
                    rams = self.session.query(RAM).where(RAM.freq >= 3000).where(RAM.freq <= 3500).all()
                    for lot in lots:
                        for ram in rams:
                            if lot.RAM_id == ram.RAM_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 5:  # freq >3500
                    rams = self.session.query(RAM).where(RAM.freq >= 3500).all()
                    for lot in lots:
                        for ram in rams:
                            if lot.RAM_id == ram.RAM_id:
                                    self.sort_lot(lot)
        elif self.componentBox.currentIndex() == 6: # Dudes wednesday
            # Уровень характеристик
            if self.parametrBox.currentIndex() == 1:  # Mem___SATA?
                # Уровень Значений
                mems = self.session.query(Memory).all()
                if self.valueBox.currentIndex() == 1:  # HDD 3.5''
                    for lot in lots:
                        for mem in mems:
                            if "HDD / 3.5''" == mem.mem_type:
                                if lot.mem_id == mem.mem_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2:  # SSD 2.5''
                    for lot in lots:
                        for mem in mems:
                            if "SSD / 2.5''" == mem.mem_type:
                                if lot.mem_id == mem.mem_id:
                                    self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3:  # SSD M.2
                    for lot in lots:
                        for mem in mems:
                            if "SSD / M.2" == mem.mem_type:
                                if lot.mem_id == mem.mem_id:
                                    self.sort_lot(lot)
            elif self.parametrBox.currentIndex() == 2:  # Mem___Volume
                # Уровень Значений
                if self.valueBox.currentIndex() == 1:  # volume <=250
                    for lot in lots:
                        mems = self.session.query(Memory).where(Memory.volume <= 250).all()
                        for mem in mems:
                            if lot.mem_id == mem.mem_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2:  # volume 250-500
                    for lot in lots:
                        mems = self.session.query(Memory).where(Memory.volume >= 250).where(Memory.volume <= 500).all()
                        for mem in mems:
                            if lot.mem_id == mem.mem_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3:  # volume 500-1000
                    for lot in lots:
                        mems = self.session.query(Memory).where(Memory.volume >= 500).where(Memory.volume <= 1000).all()
                        for mem in mems:
                            if lot.mem_id == mem.mem_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4:  # volume >=1000
                    for lot in lots:
                        mems = self.session.query(Memory).where(Memory.volume >= 1000).all()
                        for mem in mems:
                            if lot.mem_id == mem.mem_id:
                                self.sort_lot(lot)
            elif self.parametrBox.currentIndex() == 3:  # # Mem___sonic
                # Уровень Значений
                if self.valueBox.currentIndex() == 1:  # speed <=250
                    for lot in lots:
                        mems = self.session.query(Memory).where(Memory.speed <= 250).all()
                        for mem in mems:
                            if lot.mem_id == mem.mem_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2:  # speed 250-500
                    for lot in lots:
                        mems = self.session.query(Memory).where(Memory.speed >= 250).where(Memory.speed <= 500).all()
                        for mem in mems:
                            if lot.mem_id == mem.mem_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3:  # speed 500-1000
                    for lot in lots:
                        mems = self.session.query(Memory).where(Memory.speed >= 500).where(Memory.speed <= 1000).all()
                        for mem in mems:
                            if lot.mem_id == mem.mem_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4:  # speed >=1000
                    for lot in lots:
                        mems = self.session.query(Memory).where(Memory.speed >= 1000).all()
                        for mem in mems:
                            if lot.mem_id == mem.mem_id:
                                self.sort_lot(lot)
        elif self.componentBox.currentIndex() == 7: # PU
            # Уровень характеристик
            if self.parametrBox.currentIndex() == 1:  # Watt
                # Уровень Значений
                if self.valueBox.currentIndex() == 1:  # watt <=250
                    for lot in lots:
                        pus = self.session.query(PU).where(PU.watt <= 250).all()
                        for pu in pus:
                            if lot.PU_id == pu.PU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 2:  # watt 250-500
                    for lot in lots:
                        pus = self.session.query(PU).where(PU.watt >= 250).where(PU.watt <= 500).all()
                        for pu in pus:
                            if lot.PU_id == pu.PU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 3:  # watt 500-750
                    for lot in lots:
                        pus = self.session.query(PU).where(PU.watt >= 500).where(PU.watt <= 750).all()
                        for pu in pus:
                            if lot.PU_id == pu.PU_id:
                                self.sort_lot(lot)
                elif self.valueBox.currentIndex() == 4:  # watt >750
                    for lot in lots:
                        pus = self.session.query(PU).where(PU.watt >= 750).all()
                        for pu in pus:
                            if lot.PU_id == pu.PU_id:
                                self.sort_lot(lot)

    def sort_lot(self, lot: Lot):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setItem(row_position, 0, QTableWidgetItem(str(lot.lot_id)))
        self.tableWidget.setItem(row_position, 1, QTableWidgetItem(
            f"{lot.seller.user.last_name} {lot.seller.user.first_name} {lot.seller.user.patronymic if lot.seller.user.patronymic else ''}"))
        self.tableWidget.setItem(row_position, 2, QTableWidgetItem(lot.component_name()))
        self.tableWidget.setItem(row_position, 3, QTableWidgetItem(str(lot.price)))
        self.tableWidget.setItem(row_position, 4, QTableWidgetItem(str(lot.count)))