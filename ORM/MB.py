from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database_meta import Base


class MB(Base):
    __tablename__ = "MB"

    MB_id = Column(Integer, primary_key=True, autoincrement=True)
    MB_name = Column(String(63), primary_key=False, nullable=False)
    form_factor = Column(String(31), primary_key=False, nullable=False)
    socket_type = Column(String(31), primary_key=False, nullable=False)
    RAM_type = Column(String(31), primary_key=False, nullable=False)
    RAM_count = Column(Integer, primary_key=False, nullable=False)
    freq = Column(Integer, primary_key=False, nullable=False)
    GPU_type = Column(String(31), primary_key=False, nullable=False)

    lots = relationship("Lot", back_populates="MB")

    MB_CPUs = relationship("CPU_MB", back_populates="MB")
    MB_GPUs = relationship("GPU_MB", back_populates="MB")
    MB_RAMs = relationship("RAM_MB", back_populates="MB")
    MB_coolers = relationship("Cooler_MB", back_populates="MB")

    def __str__(self):
        return f"MB {self.MB_id} {self.MB_name} {self.form_factor} {self.socket_type} {self.RAM_type} {self.RAM_count} {self.freq} {self.GPU_type}"

    def __repr__(self):
        return str(self)
