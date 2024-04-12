from typing import Iterable, Callable

from PyQt5.QtWidgets import QWidget, QDialog

from ORM import get_session, Lot, User
from ui_qt import UiAddLotForm
#from .dialog import Dialog
class LotAdd(QWidget, UiAddLotForm):
    def __init__(self, callbacks: Iterable[Callable]):
        super().__init__()
        self.callbacks = callbacks
        self.setupUi(self)
        self.session = get_session()
        self.push_button_create.clicked.connect(self.create_lot) #Создание окна
        # self.comboBox.clicked.connect(self.create_lot)  # Создание окна
        self.push_button_close.clicked.connect(lambda: self.close()) #Закрытие окна
        self.comboBox.removeItem()

    def __init__(self, callbacks: Iterable[Callable]):
        super().__init__()
        self.callbacks = callbacks
        self.setupUi(self)
        self.session = get_session()
        self.push_button_create.clicked.connect(self.create_lot)  # Создание окна
        self.push_button_close.clicked.connect(lambda: self.close()) #Закрытие окна
        self.comboBox.removeItem(7)

        self.comboBox.activated.connect(self.activated)
        self.comboBox.currentTextChanged.connect(self.text_changed)
        self.comboBox.currentIndexChanged.connect(self.index_changed)

    def activated(Self, index):
        print("Activated index:", index)

    def text_changed(self, s):
        print("Text changed:", s)

    def index_changed(self, index):
        print("Index changed", index)

    def check_index(self, index):
        CurIndex = self.combobox.currentIndex()
        print(f"Index signal: {index}, currentIndex {CurIndex}")

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