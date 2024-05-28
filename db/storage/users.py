from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from db.models import AdminORM, CommonORM


def get_admin(
    login: str, password: str, session: Session
) -> list[Row]:

    query = (
        select(AdminORM.a_id)
        .where(AdminORM.a_id == login,
               AdminORM.a_pass == password)
    )
    found_users = session.execute(query)
    return found_users.first()


def get_common(
    login: str, password: str, session: Session
) -> list[Row]:

    query = (
        select(CommonORM.u_id, CommonORM.u_rights)
        .where(CommonORM.u_id == login,
               CommonORM.u_pass == password)
    )
    found_users = session.execute(query)
    return found_users.first()


def get_all_common(session: Session):
    query = (
        select(CommonORM.u_id)
    )
    found_users = session.execute(query)
    return found_users.all()