from sqlalchemy import Column, Integer, Float, ForeignKey
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

    def component_name(self):
        if self.CPU is not None:
            name = self.CPU.CPU_name
        elif self.GPU is not None:
            name = self.GPU.GPU_name
        elif self.MB is not None:
            name = self.MB.MB_name
        elif self.RAM is not None:
            name = self.RAM.RAM_name
        elif self.PU is not None:
            name = self.PU.PU_name
        elif self.memory is not None:
            name = self.memory.mem_name
        else:
            name = self.cooler.cooler_name
        return name

    def component_TC(self):
        if self.CPU is not None:
            TC = self.CPU.TC()
        elif self.GPU is not None:
            TC = self.GPU.TC()
        elif self.MB is not None:
            TC = self.MB.TC()
        elif self.RAM is not None:
            TC = self.RAM.TC()
        elif self.PU is not None:
            TC = self.PU.TC()
        elif self.memory is not None:
            TC = self.memory.TC()
        else:
            TC = self.cooler.TC()
        return TC

    def __str__(self):
        return f"Lot {self.lot_id} {self.seller_id} {self.price}"

    def __repr__(self):
        return str(self)
