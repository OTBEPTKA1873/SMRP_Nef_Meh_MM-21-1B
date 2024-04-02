from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database_meta import Base


class RAM(Base):
    __tablename__ = "RAM"

    RAM_id = Column(Integer, primary_key=True, autoincrement=True)
    RAM_name = Column(String(63), primary_key=False, nullable=False)
    RAM_type = Column(String(31), primary_key=False, nullable=False)
    volume = Column(Integer, primary_key=False, nullable=False)
    freq = Column(Integer, primary_key=False, nullable=False)

    lots = relationship("Lot", back_populates="RAM")

    RAM_MBs = relationship("RAM_MB", back_populates="RAM")

    def __str__(self):
        return f"RAM {self.RAM_id} {self.RAM_name} {self.RAM_type} {self.volume} {self.freq}"

    def __repr__(self):
        return str(self)
