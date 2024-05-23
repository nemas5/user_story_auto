from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER
from sqlalchemy.orm import relationship

from db.models import Base


class ScenarioMainsORM(Base):
    __tablename__ = "scenario_mains"

    sm_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    sm_enabled = Column(INTEGER, nullable=False)
    s_id = Column(INTEGER, ForeignKey("scenario.s_id", ondelete="CASCADE"), nullable=False)
    p_id = Column(INTEGER, ForeignKey("pattern.p_id", ondelete="CASCADE"))
    scenario = relationship("ScenarioORM", back_populates="mains")
    subs = relationship("ScenarioSubsORM", back_populates="main")
    pattern = relationship("PatternORM", back_populates="mains")
