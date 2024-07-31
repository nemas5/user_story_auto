from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER
from sqlalchemy.orm import relationship

from db.models import Base


class PatternSubsORM(Base):
    __tablename__ = "pattern_subs"

    ps_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    ps_name = Column(VARCHAR(45), nullable=False)
    p_id = Column(INTEGER, ForeignKey("pattern.p_id", ondelete="CASCADE"), nullable=False)
    pattern = relationship("PatternORM", back_populates="subs")
    subs = relationship("PatternSubs2ORM", back_populates="sub")


class PatternSubs2ORM(Base):
    __tablename__ = "pattern_subs2"

    ps2_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    ps2_name = Column(VARCHAR(45), nullable=False)
    ps_id = Column(INTEGER, ForeignKey("pattern_subs.ps_id", ondelete="CASCADE"), nullable=False)
    sub = relationship("PatternSubsORM", back_populates="subs")
