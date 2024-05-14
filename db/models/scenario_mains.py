from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER

from db.models import Base


class ScenarioMainsORM(Base):
    __tablename__ = "scenario_mains"

    sm_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    sm_enabled = Column(INTEGER, nullable=False)
    s_id = Column(INTEGER, ForeignKey("scenarios.s_id"), nullable=False)
    p_id = Column(INTEGER, ForeignKey("pattern.p_id"))
