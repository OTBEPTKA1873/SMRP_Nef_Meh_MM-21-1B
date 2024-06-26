from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database_meta import Base


class Memory(Base):
    __tablename__ = "Memory"

    mem_id = Column(Integer, primary_key=True, autoincrement=True)
    mem_name = Column(String(63), primary_key=False, nullable=False)
    mem_type = Column(String(31), primary_key=False, nullable=False)
    volume = Column(Integer, primary_key=False, nullable=False)
    speed = Column(Integer, primary_key=False, nullable=False)

    lots = relationship("Lot", back_populates="memory")

    def TC(self):
        return f"Тип: {str(self.mem_type)}\nОбъём: {str(self.volume)}\nСкорость: {str(self.speed)}"

    def __str__(self):
        return f"Memory {self.mem_id} {self.mem_name} {self.mem_type} {self.volume} {self.speed}"

    def __repr__(self):
        return str(self)
