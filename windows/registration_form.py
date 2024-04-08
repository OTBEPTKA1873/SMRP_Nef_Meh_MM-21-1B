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
        # users = self.session.query(User).all()
        # if login in [user.user_login for user in users] and password in [user.user_password for user in users]:
        user = self.session.query(User).where(User.user_login == login and User.user_password == password).first()
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
                new_seller = Seller()
                self.session.add(new_seller)
                self.session.commit()
                new_buyer = Buyer()
                self.session.add(new_buyer)
                self.session.commit()
                new_user.seller_id = new_seller.seller_id
                new_user.buyer_id = new_buyer.buyer_id
                self.session.add(new_user)
                self.session.commit()
                self.custom_close(new_user)
            else:
                dialog = Dialog("Неправильно введены данные!")
                dialog.exec_()

    def custom_close(self, user):
        for callback in self.callbacks:
            callback(user)
        self.close()
