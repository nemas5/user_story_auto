from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER
from sqlalchemy.orm import relationship

from db.models import Base


class ScenarioSubsORM(Base):
    __tablename__ = "scenario_subs"

    ss_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    ss_enabled = Column(INTEGER, nullable=False, default=0)
    sm_id = Column(INTEGER, ForeignKey("scenario_mains.sm_id", ondelete="CASCADE"), nullable=False)
    ps_id = Column(INTEGER, ForeignKey("pattern_subs.ps_id", ondelete="CASCADE"), nullable=False)
    r_id = Column(INTEGER, ForeignKey("role.r_id", ondelete="CASCADE"), nullable=False)
    main = relationship("ScenarioMainsORM", back_populates="subs")
    subs = relationship("ScenarioSubs2ORM", back_populates="sub")
    role = relationship("RoleORM", back_populates="sub")


class ScenarioSubs2ORM(Base):
    __tablename__ = "scenario_subs2"

    ss2_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    ss2_enabled = Column(INTEGER, nullable=False, default=0)
    ss_id = Column(INTEGER, ForeignKey("scenario_subs.ss_id", ondelete="CASCADE"), nullable=False)
    ps2_id = Column(INTEGER, ForeignKey("pattern_subs2.ps2_id", ondelete="CASCADE"), nullable=False)
    sub = relationship("ScenarioSubsORM", back_populates="subs")
