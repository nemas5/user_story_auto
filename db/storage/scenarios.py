from typing import Optional

from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, delete, update

from db.models import ScenarioORM, ScenarioMainsORM, \
    ScenarioSubsORM, ScenarioSubs2ORM, \
    RoleORM, PatternORM, \
    PatternSubsORM, PatternSubs2ORM


def get_scenario(scenario: int, session: Session):
    query = (
        select(ScenarioORM.s_id, ScenarioORM.s_name)
        .where(ScenarioORM.s_id == scenario)
    )
    found_scenario = session.execute(query).first()
    data = dict()
    data["id"] = found_scenario[0]
    data["name"] = found_scenario[1]
    data["components"] = list()
    query = (
        select(ScenarioMainsORM.sm_id, ScenarioMainsORM.sm_enabled,
               ScenarioMainsORM.p_id, PatternORM.p_name)
        .where(ScenarioMainsORM.s_id == found_scenario[0])
        .select_from(ScenarioMainsORM)
        .join(PatternORM, ScenarioMainsORM.p_id == PatternORM.p_id)
    )
    found_mains = session.execute(query).all()
    for main in found_mains:
        new_main = dict()
        new_main["id"] = main[0]
        new_main["enabled"] = bool(main[1])
        new_main["p_id"] = main[2]
        new_main["name"] = main[3]
        new_main["components"] = list()
        query = (
            select(ScenarioSubsORM.ss_id, ScenarioSubsORM.ss_enabled,
                   ScenarioSubsORM.ps_id, ScenarioSubsORM.r_id,
                   RoleORM.r_name, PatternSubsORM.ps_name)
            .where(ScenarioSubsORM.sm_id == main[0])
            .select_from(ScenarioSubsORM)
            .join(RoleORM, ScenarioSubsORM.r_id == RoleORM.r_id)
            .join(PatternSubsORM, ScenarioSubsORM.ps_id == PatternSubsORM.ps_id)
        )
        found_subs = session.execute(query).all()
        for sub in found_subs:
            new_sub = dict()
            new_sub["id"] = sub[0]
            new_sub["enabled"] = bool(sub[1])
            new_sub["ps_id"] = sub[2]
            new_sub["r_id"] = sub[3]
            new_sub["role"] = sub[4]
            new_sub["main"] = sub[5]
            new_sub["components"] = list()
            query = (
                select(ScenarioSubs2ORM.ss2_id, ScenarioSubs2ORM.ss2_enabled, ScenarioSubs2ORM.ps2_id)
                .where(ScenarioSubs2ORM.ss_id == sub[0])
                .select_from(ScenarioSubs2ORM)
                .join(PatternSubs2ORM, PatternSubs2ORM.ps2_id == ScenarioSubs2ORM.ps2_id)
            )
            found_subs2 = session.execute(query).all()
            for sub2 in found_subs2:
                new_sub2 = dict()
                new_sub2["id"] = sub2[0]
                new_sub2["enabled"] = bool(sub2[1])
                new_sub2["ps2_id"] = sub2[2]
                new_sub2["name"] = sub[3]
                new_sub["components"].append(new_sub2)
            new_main["components"].append(new_sub)
        data["components"].append(new_main)
    return data


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
    elif isinstance(orm_obj, ScenarioSubsORM):
        new_id = orm_obj.ss_id
    else:
        new_id = orm_obj.ss2_id
    session.commit()
    return new_id


def insert_role(role: RoleORM, session: Session) -> int:
    session.add(role)
    session.flush()
    session.refresh(role)
    new_id = role.r_id
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
