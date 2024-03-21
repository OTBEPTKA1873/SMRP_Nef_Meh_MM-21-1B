from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database_meta import Base


class Buyer(Base):
    __tablename__ = "Buyer"

    buyer_id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String(31), primary_key=False, nullable=False)
    last_name = Column(String(31), primary_key=False, nullable=False)
    patronymic = Column(String(31), primary_key=False, nullable=True)
    registration_date = Column(String(31), primary_key=False, nullable=True)

    receipts = relationship("Receipt", back_populates="buyer")

    def __str__(self):
        return f"Buyer {self.buyer_id} {self.first_name} {self.last_name} {self.patronymic} {self.registration_date}"

    def __repr__(self):
        return str(self)
