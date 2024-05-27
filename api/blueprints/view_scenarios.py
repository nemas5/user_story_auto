import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for

from db.storage import get_scenario_by_user, delete_scenario
from db.connection import get_session
from db.models import ScenarioORM, ScenarioMainsORM, ScenarioSubsORM
from db.storage import update_scenario, update_scenario_main, update_scenario_sub
from utilities.scenarios import Scenario
from utilities.patterns import pattern_list

blueprint_view = Blueprint('bp_view', __name__)


@blueprint_view.route('/view', methods=['GET'])
def view_scenarios():
    db_session = get_session()
    user = session["user_id"]
    s_id, s_name = get_scenario_by_user(user, db_session)
    return {"name": s_id, "scenario": s_name}


@blueprint_view.route('/edit/<s_id>', methods=['GET'])
def edit_scenario(s_id: int):
    db_session = get_session()
    if request.method == 'GET':
        new = Scenario(s_id)
        mheaders = {i.pattern: i.name for i in pattern_list}
        sheaders = {i.pattern: i.get_headers() for i in pattern_list}
        return {"mains": new.mains, "subs": new.subs, "name": new.name,
                "mheaders": mheaders, "sheaders": sheaders}
    else:
        new = Scenario(s_id)
        new_sc = ScenarioORM(s_id=s_id, s_name=new.name)
        update_scenario(new_sc, db_session)
        for main in new.mains.keys():
            new_main = ScenarioMainsORM(sm_enabled=new.mains[main],
                                        s_id=s_id,
                                        p_id=main)
            new_main_id = update_scenario_main(new_main, db_session)
            for sub in new.subs[main].keys():
                new_sub = ScenarioSubsORM(ss_enabled=new.subs[main][sub],
                                          sm_id=new_main_id,
                                          ps_id=sub)
                update_scenario_sub(new_sub, db_session)
        new.build_docx(session["user_id"])
        return {"response": 1}


@blueprint_view.route('/delete/<s_id>', methods=['DELETE'])
def sc_delete(s_id: int):
    db_session = get_session()
    delete_scenario(s_id, db_session)
    return {"response": 1}
