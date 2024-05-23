from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER

from db.models import Base


class ScenarioSubsORM(Base):
    __tablename__ = "scenario_subs"

    ss_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    ss_enabled = Column(INTEGER, nullable=False, default=0)
    sm_id = Column(INTEGER, ForeignKey("scenario_mains.sm_id", ondelete="CASCADE"), nullable=False)
    ps_id = Column(INTEGER, ForeignKey("pattern_subs.ps_id", ondelete="CASCADE"), nullable=False)
