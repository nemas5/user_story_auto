from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER

from db.models import Base


class RoleORM(Base):
    __tablename__ = "role"

    r_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    s_id = Column(INTEGER, ForeignKey("scenario.s_id", ondelete="CASCADE"), nullable=False)
    r_name = Column(VARCHAR, nullable=False)
