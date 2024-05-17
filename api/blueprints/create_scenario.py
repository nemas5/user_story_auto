import os
from typing import Optional
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for

from db.storage import get_admin, get_common, insert_scenario
from db.connection import get_session
from db.models import ScenarioORM, ScenarioMainsORM, ScenarioSubsORM
from utilities.scenarios import Scenario

blueprint_create = Blueprint('bp_create', __name__)
db_session = get_session()


@blueprint_create.route('/roles/<scenario>', methods=['GET', 'POST'])
def create_scenario(scenario: Optional[dict] = None):
    if request.method == 'GET':
        if scenario is None:
            new = Scenario()
        else:
            new = Scenario(scenario)
        return {"mains": new.mains, "subs": new.subs, "name": new.name}
    else:
        new = Scenario(scenario)
        new_sc = ScenarioORM(s_name=new.name, u_id=session["user_id"])
        new_sc_id = insert_scenario(new_sc, db_session)
        for main in new.mains.keys():
            new_main = ScenarioMainsORM(sm_enabled=new.mains[main],
                                        s_id=new_sc_id,
                                        p_id=main)
            new_main_id = insert_scenario(new_main, db_session)
            for sub in new.subs[main].keys():
                new_sub = ScenarioSubsORM(ss_enabled=new.subs[main][sub],
                                          sm_id=new_main_id,
                                          ps_id=sub)
                insert_scenario(new_sub, db_session)
        new.build_docx(session["user_id"])
        return {"response": 1}
