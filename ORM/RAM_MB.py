from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database_meta import Base


class RAM_MB(Base):
    __tablename__ = "RAM_MB"

    RAM_id = Column(String(63), ForeignKey("RAM.RAM_id"), primary_key=True, nullable=False)
    MB_id = Column(String(63), ForeignKey("MB.MB_name"), primary_key=True, nullable=False)

    RAM = relationship("RAM", back_populates="RAM_MBs")
    MB = relationship("MB", back_populates="MB_RAMs")

    def __repr__(self):
        return str(self)
