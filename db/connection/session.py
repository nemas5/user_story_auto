from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import get_db_settings
from db.models import Base

settings = get_db_settings()
DATABASE_URL = settings.db_url
# DATABASE_URL = f"mysql+pymysql://root:qwerty@127.0.0.1:3306/diploma"

engine = create_engine(DATABASE_URL)
db_session = sessionmaker(engine, class_=Session)


'''
def init_db() -> None:

    with engine.begin() as conn:
        conn.run_sync(Base.metadata.drop_all)
        conn.run_sync(Base.metadata.create_all)
'''


def get_session():

    with db_session() as db_sess:
        return db_sess


'''
from sqlalchemy.sql import select
from db.models.admin_user import AdminORM
ses = get_session()
query = (
        select(AdminORM.a_id,)
    )
tag_list = ses.execute(query)
for i in tag_list:
    print(i)
'''

