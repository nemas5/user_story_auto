from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import relationship

from db.models import Base


class CommonORM(Base):
    __tablename__ = "common_user"

    u_id = Column(VARCHAR(15), primary_key=True, nullable=False)
    u_pass = Column(VARCHAR(15), nullable=False)
    u_rights = Column(VARCHAR(15), nullable=False)
    scenarios = relationship("ScenarioORM", back_populates="user")
