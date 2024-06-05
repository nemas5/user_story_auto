import os
from flask import Blueprint, render_template, request, jsonify, session, make_response

from db.storage import get_scenario_by_user, delete_scenario
from db.connection import get_session
from db.models import ScenarioORM, ScenarioMainsORM, ScenarioSubsORM
from db.storage import update_scenario, update_scenario_main, update_scenario_sub, get_roles_by_scenario
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
