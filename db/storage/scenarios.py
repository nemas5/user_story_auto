from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

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
