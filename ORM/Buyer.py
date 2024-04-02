from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database_meta import Base


class Buyer(Base):
    __tablename__ = "Buyer"

    buyer_id = Column(Integer, primary_key=True, autoincrement=True)

    receipts = relationship("Receipt", back_populates="buyer")

    user = relationship("User", back_populates="buyer")

    def __str__(self):
        return f"Buyer {self.buyer_id} {self.first_name} {self.last_name} {self.patronymic} {self.registration_date}"

    def __repr__(self):
        return str(self)
