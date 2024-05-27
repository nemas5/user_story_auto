from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from db.models import PatternORM, PatternSubsORM, PatternSubs2ORM


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
    data = list()
    for i in range(len(found_subs)):
        sub = found_subs[i]
        new = dict()
        new["id"] = sub[0]
        new["name"] = sub[1]
        new["components"] = list()
        query = (
            select(PatternSubs2ORM.ps2_id, PatternSubs2ORM.ps2_name)
            .where(PatternSubs2ORM.ps_id == new["id"])
        )
        found_subs2 = session.execute(query).all()
        for j in range(len(found_subs2)):
            sub2 = found_subs2[j]
            new2 = dict()
            new2["id"] = sub2[0]
            new2["name"] = sub2[1]
            new["components"].append(new2)
            new2["doc"] = f'{i+1}/{j+1}.docx'
        data.append(new)
    return data
