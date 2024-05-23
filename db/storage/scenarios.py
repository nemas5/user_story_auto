from typing import Optional

from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, delete, update

from db.models import ScenarioORM, ScenarioMainsORM, ScenarioSubsORM


def get_scenario(scenario: int, session: Session):
    query = (
        select(ScenarioORM.s_id, ScenarioORM.s_name)
        .where(ScenarioORM.s_id == scenario)
    )
    found_scenario = session.execute(query).first()
    return found_scenario


def get_scenario_mains(main: int, session: Session):
    query = (
        select(ScenarioMainsORM.sm_id, ScenarioMainsORM.sm_enabled, ScenarioMainsORM.p_id)
        .where(ScenarioMainsORM.sm_id == main)
    )
    found_mains = session.execute(query).all()
    return found_mains


def get_scenario_subs(sub: int, session: Session):
    query = (
        select(ScenarioSubsORM.ss_id, ScenarioSubsORM.ss_enabled, ScenarioSubsORM.ps_id)
        .where(ScenarioSubsORM.sm_id == sub)
    )
    found_subs = session.execute(query).all()
    return found_subs


def get_scenario_by_user(user: str, session: Session):
    pass


def insert_scenario(orm_obj,
                    session: Session) -> int:
    session.add(orm_obj)
    session.flush()
    session.refresh(orm_obj)
    if isinstance(orm_obj, ScenarioORM):
        new_id = orm_obj.s_id
    elif isinstance(orm_obj, ScenarioMainsORM):
        new_id = orm_obj.sm_id
    else:
        new_id = orm_obj.ss_id
    session.commit()
    return new_id


def update_scenario(s_orm: ScenarioORM, session: Session):
    query = (update(ScenarioORM).where(ScenarioORM.s_id == s_orm.s_id).values(s_name=s_orm.name))
    session.execute(query)
    session.commit()


def update_scenario_sub(ss_orm: ScenarioSubsORM, session: Session):
    query = (update(ScenarioSubsORM)
             .where(ScenarioSubsORM.sm_id == ss_orm.sm_id,
                    ScenarioSubsORM.ps_id == ss_orm.ps_id)
             .values(sm_enabled=ss_orm.sm_enabled))
    session.execute(query)
    session.commit()


def update_scenario_main(sm_orm: ScenarioMainsORM, session: Session) -> int:
    query = (update(ScenarioMainsORM)
             .where(ScenarioMainsORM.s_id == sm_orm.s_id,
                    ScenarioMainsORM.p_id == sm_orm.p_id)
             .values(sm_enabled=sm_orm.sm_enabled))
    session.execute(query)
    session.commit()
    query = (
        select(ScenarioMainsORM.s_id)
        .where(ScenarioMainsORM.s_id == sm_orm.s_id,
               ScenarioMainsORM.p_id == sm_orm.p_id)
    )
    found_scenario = session.execute(query).first()
    return found_scenario[0]


def delete_scenario(scenario: int, session: Session):
    query = (delete(ScenarioORM).where(ScenarioORM.s_id == scenario))
    session.execute(query)
    session.commit()
