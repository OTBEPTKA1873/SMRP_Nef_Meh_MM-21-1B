from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database_meta import Base


class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_login = Column(String(31), primary_key=False, nullable=False)
    user_password = Column(String(31), primary_key=False, nullable=False)

    first_name = Column(String(31), primary_key=False, nullable=False)
    last_name = Column(String(31), primary_key=False, nullable=False)
    patronymic = Column(String(31), primary_key=False, nullable=True)

    seller_id = Column(Integer, ForeignKey("Seller.seller_id"))
    buyer_id = Column(Integer, ForeignKey("Buyer.buyer_id"))

    seller = relationship("Seller", back_populates="user")
    buyer = relationship("Buyer", back_populates="user")

    def __repr__(self):
        return str(self)
