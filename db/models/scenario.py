from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER
from sqlalchemy.orm import relationship

from db.models import Base


class ScenarioORM(Base):
    __tablename__ = "scenario"

    s_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    s_name = Column(VARCHAR(45), nullable=False)
    u_id = Column(INTEGER, ForeignKey("common_user.u_id", ondelete="CASCADE"))
    mains = relationship("ScenarioMainsORM", back_populates="scenario")
    role = relationship("RoleORM", back_populates="scenario")
    user = relationship("CommonORM", back_populates="scenarios")
