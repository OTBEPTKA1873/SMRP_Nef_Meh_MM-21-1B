from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database_meta import Base


class CPU(Base):
    __tablename__ = "CPU"

    CPU_id = Column(Integer, primary_key=True, autoincrement=True)
    CPU_name = Column(String(63), primary_key=False, nullable=False)
    ALU = Column(Integer, primary_key=False, nullable=False)
    freq = Column(Integer, primary_key=False, nullable=False)
    socket = Column(String(31), primary_key=False, nullable=False)
    TDP = Column(Integer, primary_key=False, nullable=False)

    lots = relationship("Lot", back_populates="CPU")

    CPU_MBs = relationship("CPU_MB", back_populates="CPU")

    def __str__(self):
        return f"CPU {self.CPU_id} {self.CPU_name} {self.ALU} {self.freq} {self.socket} {self.TDP}"

    def __repr__(self):
        return str(self)
