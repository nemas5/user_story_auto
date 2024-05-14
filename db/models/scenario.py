from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER

from db.models import Base


class ScenarioORM(Base):
    __tablename__ = "scenario"

    s_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    s_name = Column(VARCHAR(45), nullable=False)
    u_id = Column(INTEGER)
