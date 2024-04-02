from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database_meta import Base


class Cooler_MB(Base):
    __tablename__ = "Cooler_MB"

    cooler_id = Column(Integer, ForeignKey("Cooler.cooler_id"), primary_key=True, nullable=False)
    MB_id = Column(Integer, ForeignKey("MB.MB_id"), primary_key=True, nullable=False)

    cooler = relationship("Cooler", back_populates="cooler_MBs")
    MB = relationship("MB", back_populates="MB_coolers")

    def __repr__(self):
        return str(self)
