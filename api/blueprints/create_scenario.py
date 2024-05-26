import os
from typing import Optional
from flask import Blueprint, render_template, request, current_app, session, jsonify, make_response

from db.storage import get_admin, get_common, insert_scenario
from db.connection import get_session
from db.models import ScenarioORM, ScenarioMainsORM, ScenarioSubsORM
from utilities.scenarios import Scenario
from utilities.patterns import pattern_list

blueprint_create = Blueprint('bp_create', __name__)
db_session = get_session()


@blueprint_create.route('/create', methods=['GET', 'POST'])
def create_scenario():
    if request.method == 'GET':
        new = Scenario()

        return make_response(jsonify({}), 200)
    else:
        scenario = request.json()
        print(scenario)
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


@blueprint_create.route('/role', methods=['GET', 'POST'])
def scenario_roles():
    if request.method == 'GET':
        pass
    else:
        print(request.json)

