import os
from flask import Blueprint, render_template, request, jsonify, session, make_response

from db.storage import get_scenario_by_user, delete_scenario
from db.connection import get_session
from db.models import ScenarioORM, ScenarioMainsORM, ScenarioSubsORM, RoleORM
from db.storage import update_scenario, update_scenario_main, \
    update_scenario_sub, get_roles_by_scenario, \
    insert_role, update_role, update_scenario_sub2, delete_role
from utilities.scenarios import Scenario
from utilities.patterns import pattern_list

blueprint_view = Blueprint('bp_view', __name__)


@blueprint_view.route('/view', methods=['GET'])
def view_scenarios():
    db_session = get_session()
    user = session["user_id"]
    scenarios = get_scenario_by_user(user, db_session)
    res = [{"id": scenario[0], "name": scenario[1]} for scenario in scenarios]
    return make_response(jsonify(res), 200)


@blueprint_view.route('/edit/<s_id>', methods=['GET', 'POST'])
def edit_scenario(s_id: int):
    if request.method == 'GET':
        new = Scenario(s_id, session["user_id"])
        return make_response(jsonify({'data': new.data, 'name': new.name}), 200)
    else:
        db_session = get_session()
        print(request.json["systems"])
        print(request.json["roles"])
        print(request.json["roles"]["deletedRoles"])
        update_scenario(request.json["s_id"], request.json["name"], db_session)
        roles = dict()
        for role in request.json["roles"]["newRoles"]:
            new_role = RoleORM(s_id=request.json["s_id"], r_name=role)
            new_role_id = insert_role(new_role, db_session)
            roles[role] = new_role_id
        for role in request.json["roles"]["updatedRoles"].keys():
            update_role(role, request.json["roles"]["updatedRoles"][role], db_session)
        for main in request.json["systems"]:
            globool1 = True and main['enabled']
            update_scenario_main(main["id"], globool1, db_session)
            for sub in main["components"]:
                globool2 = sub["enabled"] and globool1
                r_id = str(sub["r_id"])
                if r_id in request.json["roles"]["deletedRoles"]:
                    flag = True
                    for i in request.json["roles"]["updatedRoles"].keys():
                        if request.json["roles"]["updatedRoles"][i] == "Любой пользователь":
                            r_id = i
                            flag = False
                            break
                    if flag:
                        new_role = RoleORM(s_id=request.json["s_id"], r_name="Любой пользователь")
                        new_role_id = insert_role(new_role, db_session)
                        request.json["roles"]["updatedRoles"][new_role_id] = "Любой пользователь"
                        r_id = new_role_id
                if sub["role"] in roles:
                    r_id = roles[sub["role"]]
                update_scenario_sub(sub["id"], r_id, globool2, db_session)
                for sub2 in sub["components"]:
                    globool3 = sub2["enabled"] and globool2
                    update_scenario_sub2(sub2["id"], globool3, db_session)
        for role in request.json["roles"]["deletedRoles"]:
            delete_role(role, db_session)
        sc = Scenario(request.json["s_id"], session["user_id"])
        print(sc.data)
        sc.build_docx()
        return make_response(jsonify(
            {'documentUrl': f'http://localhost:3000/api/download/download/{request.json["s_id"]}'}
        ), 200)


@blueprint_view.route('/delete/<s_id>', methods=['DELETE'])
def sc_delete(s_id: int):
    db_session = get_session()
    delete_scenario(s_id, db_session)
    return {"response": 1}


@blueprint_view.route('/role/<s_id>', methods=['GET', 'POST'])
def scenario_roles(s_id: int):
    db_session = get_session()
    roles = get_roles_by_scenario(s_id, db_session)
    res = {role[0]: role[1] for role in roles}
    return make_response(jsonify(res), 200)
