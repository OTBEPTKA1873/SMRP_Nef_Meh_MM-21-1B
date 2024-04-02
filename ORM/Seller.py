from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database_meta import Base


class Seller(Base):
    __tablename__ = "Seller"

    seller_id = Column(Integer, primary_key=True, autoincrement=True)

    lots = relationship("Lot", back_populates="seller")

    user = relationship("User", back_populates="seller")

    def __str__(self):
        return f"Seller {self.seller_id} {self.first_name} {self.last_name} {self.patronymic} {self.registration_date}"

    def __repr__(self):
        return str(self)
