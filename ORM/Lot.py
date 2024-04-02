from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .database_meta import Base


class Lot(Base):
    __tablename__ = "Lot"

    lot_id = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(Integer, ForeignKey("Seller.seller_id"))
    price = Column(Float, primary_key=False, nullable=False)
    GPU_id = Column(Integer, ForeignKey("GPU.GPU_id"))
    CPU_id = Column(Integer, ForeignKey("CPU.CPU_id"))
    MB_id = Column(Integer, ForeignKey("MB.MB_id"))
    RAM_id = Column(Integer, ForeignKey("RAM.RAM_id"))
    PU_id = Column(Integer, ForeignKey("PU.PU_id"))
    mem_id = Column(Integer, ForeignKey("Memory.mem_id"))
    cooler_id = Column(Integer, ForeignKey("Cooler.cooler_id"))
    count = Column(Integer, primary_key=False, nullable=False)

    receipts = relationship("Receipt", back_populates="lot")
    seller = relationship("Seller", back_populates="lots")

    CPU = relationship("CPU", back_populates="lots")
    GPU = relationship("GPU", back_populates="lots")
    MB = relationship("MB", back_populates="lots")
    RAM = relationship("RAM", back_populates="lots")
    PU = relationship("PU", back_populates="lots")
    memory = relationship("Memory", back_populates="lots")
    cooler = relationship("Cooler", back_populates="lots")

    def __str__(self):
        return f"Lot {self.Lot_id} {self.seller_id} {self.price} {self.GPU_id} {self.CPU_id} {self.MB_id} {self.RAM_id} {self.PowerUnit_id} {self.Mem_id} {self.Cooler_id}"

    def __repr__(self):
        return str(self)
