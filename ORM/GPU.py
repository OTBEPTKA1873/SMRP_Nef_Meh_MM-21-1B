from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database_meta import Base


class GPU(Base):
    __tablename__ = "GPU"

    GPU_id = Column(Integer, primary_key=True, autoincrement=True)
    GPU_name = Column(String(63), primary_key=False, nullable=False)
    freq = Column(Integer, primary_key=False, nullable=False)
    ALU = Column(Integer, primary_key=False, nullable=False)
    volume = Column(Integer, primary_key=False, nullable=False)
    GPU_type = Column(String(31), primary_key=False, nullable=False)

    lots = relationship("Lot", back_populates="GPU")

    GPU_MBs = relationship("GPU_MB", back_populates="GPU")

    def __str__(self):
        return f"GPU {self.GPU_id} {self.GPU_name} {self.freq} {self.ALU} {self.volume} {self.GPU_type}"

    def __repr__(self):
        return str(self)
