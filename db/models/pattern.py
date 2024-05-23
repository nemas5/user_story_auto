from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER
from sqlalchemy.orm import relationship

from db.models import Base


class PatternORM(Base):
    __tablename__ = "pattern"

    p_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    p_name = Column(VARCHAR(45), nullable=False)
    subs = relationship("PatternSubsORM", back_populates="pattern")
    mains = relationship("ScenarioMainsORM", back_populates="pattern")
