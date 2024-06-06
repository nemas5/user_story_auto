import os
from typing import Optional
from flask import Blueprint, request, session, jsonify, make_response, send_file

from db.storage import get_admin, get_common, insert_scenario, insert_role
from db.connection import get_session
from db.models import ScenarioORM, ScenarioMainsORM, ScenarioSubsORM, ScenarioSubs2ORM, RoleORM
from utilities.scenarios import Scenario
from utilities.patterns import pattern_list

blueprint_create = Blueprint('bp_create', __name__)


@blueprint_create.route('/create', methods=['GET', 'POST'])
def create_scenario():
    if request.method == 'GET':
        new = Scenario(user=session["user_id"])
        print(new.data)
        return make_response(jsonify(new.data), 200)
    else:
        db_session = get_session()
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
            globool1 = True and main["enabled"]
            new_main = ScenarioMainsORM(sm_enabled=globool1,
                                        s_id=new_sc_id,
                                        p_id=main["p_id"],
                                        )
            new_main_id = insert_scenario(new_main, db_session)
            for sub in main["components"]:
                globool2 = globool1 and sub["enabled"]
                new_sub = ScenarioSubsORM(ss_enabled=globool2,
                                          sm_id=new_main_id,
                                          ps_id=sub["ps_id"],
                                          r_id=roles[sub["role"]]
                                          )
                new_sub_id = insert_scenario(new_sub, db_session)
                for sub2 in sub["components"]:
                    globool3 = globool2 and sub2["enabled"]
                    new_sub2 = ScenarioSubs2ORM(ss2_enabled=globool3,
                                                ss_id=new_sub_id,
                                                ps2_id=sub2["ps2_id"])
                    insert_scenario(new_sub2, db_session)
        sc = Scenario(new_sc_id, session["user_id"])
        print(sc.data)
        sc.build_docx()
        return make_response(jsonify(new_sc_id), 200)
