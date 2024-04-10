from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship

from .database_meta import Base


class Cooler(Base):
    __tablename__ = "Cooler"

    cooler_id = Column(Integer, primary_key=True, autoincrement=True)
    cooler_name = Column(String(63), primary_key=False, nullable=False)
    socket = Column(String(31), primary_key=False, nullable=False)
    DH = Column(Integer, primary_key=False, nullable=False)
    noise = Column(Float, primary_key=False, nullable=False)

    lots = relationship("Lot", back_populates="cooler")

    cooler_MBs = relationship("Cooler_MB", back_populates="cooler")

    def TC(self):
        return f"Сокет: {self.socket}\nDH: {str(self.DH)}\nУровень шума: {str(self.noise)}"

    def __str__(self):
        return f"Cooler {self.CL_id} {self.CL_name} {self.socket} {self.DH} {self.noise}"

    def __repr__(self):
        return str(self)
