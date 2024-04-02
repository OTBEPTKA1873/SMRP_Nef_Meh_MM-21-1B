from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database_meta import Base


class PU(Base):
    __tablename__ = "PU"

    PU_id = Column(Integer, primary_key=True, autoincrement=True)
    PU_name = Column(String(63), primary_key=False, nullable=False)
    watt = Column(Integer, primary_key=False, nullable=False)

    lots = relationship("Lot", back_populates="PU")

    def __str__(self):
        return f"Power Unit {self.PU_id} {self.PU_name} {self.watt}"

    def __repr__(self):
        return str(self)
