from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from db.models import PatternORM, PatternSubsORM


def get_pattern_list(session: Session):
    query = (
        select(PatternORM.p_id, PatternORM.p_name)
    )
    found_patterns = session.execute(query)
    return found_patterns.all()


def get_pattern(pattern: str, session: Session):
    query = (
        select(PatternSubsORM.ps_id, PatternSubsORM.ps_name)
        .where(PatternSubsORM.p_id == pattern)
    )
    found_subs = session.execute(query).all()
    return {i[0]: i[1] for i in found_subs}

