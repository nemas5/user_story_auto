from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base


metadata = MetaData()
DeclarativeBase = declarative_base(metadata=metadata)

Base = declarative_base()
