import os
from typing import Optional
from flask import Blueprint, render_template, request, current_app, session, jsonify, make_response

from db.storage import get_admin, get_common, insert_scenario, insert_role
from db.connection import get_session
from db.models import ScenarioORM, ScenarioMainsORM, ScenarioSubsORM, ScenarioSubs2ORM, RoleORM
from utilities.scenarios import Scenario
from utilities.patterns import pattern_list

blueprint_create = Blueprint('bp_create', __name__)
db_session = get_session()


@blueprint_create.route('/create', methods=['GET', 'POST'])
def create_scenario():
    if request.method == 'GET':
        new = Scenario(user=session["user_id"])

        return make_response(jsonify(new.data), 200)
    else:
        name = request.json["name"]
        scenario = request.json['systems']
        new_sc = ScenarioORM(s_name=name, u_id=session["user_id"])
        new_sc_id = insert_scenario(new_sc, db_session)
        roles = dict()
        for role in request.json["roles"]:
            new_role = RoleORM(s_id=new_sc_id, r_name=role)
            new_role_id = insert_role(new_role, db_session)
            roles[role] = new_role_id
        new_role = RoleORM(s_id=new_sc_id, r_name="Любой пользователь")
        new_role_id = insert_role(new_role, db_session)
        roles["Любой пользователь"] = new_role_id
        for main in scenario:
            new_main = ScenarioMainsORM(sm_enabled=main["enabled"],
                                        s_id=new_sc_id,
                                        p_id=main["p_id"],
                                        )
            new_main_id = insert_scenario(new_main, db_session)
            for sub in main["components"]:
                new_sub = ScenarioSubsORM(ss_enabled=sub["enabled"],
                                          sm_id=new_main_id,
                                          ps_id=sub["ps_id"],
                                          r_id=roles[sub["role"]]
                                          )
                new_sub_id = insert_scenario(new_sub, db_session)
                for sub2 in sub["components"]:
                    new_sub2 = ScenarioSubs2ORM(ss2_enabled=sub2["enabled"],
                                                ss_id=new_sub_id,
                                                ps2_id=sub2["ps2_id"])
                    insert_scenario(new_sub2, db_session)
        sc = Scenario(new_sc_id, session["user_id"])
        sc.build_docx()
        return make_response('', 200)


@blueprint_create.route('/role', methods=['GET', 'POST'])
def scenario_roles():
    if request.method == 'GET':
        pass
    else:
        print(request.json)

