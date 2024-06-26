from typing import Iterable, Callable

from PyQt5.QtWidgets import QWidget

from ORM import get_session, User, Seller, Buyer
from ui_qt import UiRegistrationForm
from .dialog import Dialog


class Registration(QWidget, UiRegistrationForm):
    def __init__(self, callbacks: Iterable[Callable]):
        super().__init__()
        self.callbacks = callbacks
        self.setupUi(self)
        self.session = get_session()

        self.pushButton.clicked.connect(self.register)

    def register(self):
        login = self.line_edit_login.text()
        password = self.line_edit_password.text()
        if len(login) == 0 or len(password) == 0:
            dialog = Dialog("Неправильно введены данные!")
            dialog.exec_()
            return
        if len(login) > 31 or len(password) > 31:
            dialog = Dialog("Превышен допустимый размер!")
            dialog.exec_()
            return

        user = self.session.query(User).where(User.user_login == login, User.user_password == password).first()
        if user is not None:
            self.custom_close(user)
        else:
            FIO = self.line_edit_FIO.text().split()
            if FIO and len(FIO) > 1:
                new_user = User(user_login=login,
                                user_password=password,
                                last_name=FIO[0],
                                first_name=FIO[1],
                                patronymic=FIO[2] if len(FIO) >= 3 else None)
                self.session.add(new_user)
                self.session.commit()
                new_seller = Seller()
                new_seller.user_id = new_user.user_id
                self.session.add(new_seller)
                self.session.commit()
                new_buyer = Buyer()
                new_buyer.user_id = new_user.user_id
                self.session.add(new_buyer)
                self.session.commit()
                self.custom_close(new_user)
            else:
                dialog = Dialog("Неправильно введены данные!")
                dialog.exec_()

    def custom_close(self, user):
        for callback in self.callbacks:
            callback(user)
        self.close()
