from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database_meta import Base


class Receipt(Base):
    __tablename__ = "Receipt"

    receipt_id = Column(Integer, primary_key=True, autoincrement=True)
    lot_id = Column(Integer, ForeignKey("Lot.lot_id"))
    buyed_count = Column(Integer, primary_key=False, nullable=True)
    buyer_id = Column(Integer, ForeignKey("Buyer.buyer_id"))
    purchase_date = Column(String(15), primary_key=False, nullable=True)

    lot = relationship("Lot", back_populates="receipts")
    buyer = relationship("Buyer", back_populates="receipts")

    def __str__(self):
        return f"Receipt {self.receipt_id} {self.lot_id} {self.buyer_id} {self.purchase_date}"

    def __repr__(self):
        return str(self)
