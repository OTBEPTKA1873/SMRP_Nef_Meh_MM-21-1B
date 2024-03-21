from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database_meta import Base


class CPU_MB(Base):
    __tablename__ = "CPU_MB"

    CPU_id = Column(String(63), ForeignKey("CPU.CPU_id"), primary_key=True, nullable=False)
    MB_id = Column(String(63), ForeignKey("MB.MB_name"), primary_key=True, nullable=False)

    CPU = relationship("CPU", back_populates="CPU_MBs")
    MB = relationship("MB", back_populates="MB_CPUs")

    def __repr__(self):
        return str(self)
