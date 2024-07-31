from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR

from db.models import Base


class AdminORM(Base):
    __tablename__ = "admin_user"

    a_id = Column(VARCHAR(15), primary_key=True, nullable=False)
    a_pass = Column(VARCHAR(15), nullable=False)
