from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog

from ORM import get_session, Lot, User
from ui_qt import UiMainWindow
from .dialog import Dialog
from .registration_form import Registration
from .add_lot_form import LotAdd
from .buy_lot_form import LotBuy
from .update_lot_form import LotUpdate
from .receipts_form import Receipts


class MainWindow(QMainWindow, UiMainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.create_window = None
        self.session = get_session()
        self.current_row = None
        self.current_user = None

        self.push_button_register.clicked.connect(self.open_register)
        self.push_button_create.clicked.connect(self.open_lot_add)
        self.push_button_buy.clicked.connect(self.open_lot_buy)
        self.tableWidget.cellDoubleClicked.connect(self.open_lot_update)
        self.push_button_receipts.clicked.connect(self.open_receipts)
        self.push_button_sort.clicked.connect(self.open_sort)
        self.tableWidget.cellClicked.connect(self.table_widget_cell_clicked)

        self.open_register()
        self.update_table()

    def update_table(self):
        lots = self.session.query(Lot).where(Lot.count > 0).order_by(Lot.lot_id).all()
        self.tableWidget.setRowCount(0)
        for lot in lots:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setItem(row_position, 0, QTableWidgetItem(f"{lot.seller.user.last_name} {lot.seller.user.first_name} {lot.seller.user.patronymic if lot.seller.user.patronymic else ''}"))
            if lot.CPU is not None:
                self.tableWidget.setItem(row_position, 1, QTableWidgetItem(lot.CPU.CPU_name))
            elif lot.GPU is not None:
                self.tableWidget.setItem(row_position, 1, QTableWidgetItem(lot.GPU.GPU_name))
            elif lot.MB is not None:
                self.tableWidget.setItem(row_position, 1, QTableWidgetItem(lot.MB.MB_name))
            elif lot.RAM is not None:
                self.tableWidget.setItem(row_position, 1, QTableWidgetItem(lot.RAM.RAM_name))
            elif lot.PU is not None:
                self.tableWidget.setItem(row_position, 1, QTableWidgetItem(lot.PU.PU_name))
            elif lot.memory is not None:
                self.tableWidget.setItem(row_position, 1, QTableWidgetItem(lot.memory.mem_name))
            else:
                self.tableWidget.setItem(row_position, 1, QTableWidgetItem(lot.cooler.cooler_name))
            self.tableWidget.setItem(row_position, 2, QTableWidgetItem(str(lot.price)))
            self.tableWidget.setItem(row_position, 3, QTableWidgetItem(str(lot.count)))

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
            return
        if self.current_row is None:
            dialog = Dialog("Выберите лот!")
            dialog.exec_()
            return
        lot_id = int(self.tableWidget.item(self.current_row, 0).text())
        lot = self.session.query(Lot).get(lot_id)
        self.create_window = LotBuy(lot, self.current_user, [self.update_table])
        self.create_window.show()

    def open_lot_update(self, row, column):
        lot_id = int(self.tableWidget.item(row, 0).text())
        lot = self.session.query(Lot).get(lot_id)
        self.create_window = LotUpdate(lot, self.current_user, [self.update_table])
        self.create_window.show()

    def open_lot_add(self):
        ...

    def open_receipts(self):
        if self.current_user is None:
            self.open_register()
            return
        self.create_window = Receipts(self.current_user)
        self.create_window.show()


    def open_sort(self):
        ...

    """def open_actor_update(self, row, column):
        actor_id = int(self.tableWidget.item(row, 0).text())
        actor = self.session.query(Actor).get(actor_id)
        self.create_window = ActorUpdate(actor, [self.updateTable])
        self.create_window.show()

    def open_dialog_delete_actor(self):
        if self.current_row is None:
            return
        dialog_delete = Dialog("Точно хотите удалить??")
        ret_value = dialog_delete.exec_()
        if ret_value == QDialog.Accepted:
            actor_id = int(self.tableWidget.item(self.current_row, 0).text())
            actor = self.session.query(Actor).get(actor_id)
            self.session.delete(actor)
            self.session.commit()
            self.update_table()"""