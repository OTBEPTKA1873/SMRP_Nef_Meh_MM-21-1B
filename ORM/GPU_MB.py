from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database_meta import Base


class GPU_MB(Base):
    __tablename__ = "GPU_MB"

    GPU_id = Column(Integer, ForeignKey("GPU.GPU_id"), primary_key=True, nullable=False)
    MB_id = Column(Integer, ForeignKey("MB.MB_id"), primary_key=True, nullable=False)

    GPU = relationship("GPU", back_populates="GPU_MBs")
    MB = relationship("MB", back_populates="MB_GPUs")

    def __repr__(self):
        return str(self)
