import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for

from db.storage import get_scenario_by_user
from db.connection import get_session
from utilities.scenarios import Scenario

blueprint_sc_view = Blueprint('sc_view', __name__)
db_session = get_session()


@blueprint_sc_view.route('/view', methods=['GET'])
def view_scenarios():
    user = session["user_id"]
    s_id, s_name = get_scenario_by_user(user, db_session)
    return s_id, s_name


@blueprint_sc_view.route('/edit/<s_id>', methods=['GET'])
def edit_scenario(s_id: int):
    scenario = Scenario(s_id)
    return scenario.mains, scenario.subs


@blueprint_sc_view.route('/delete/<s_id>', methods=['GET'])
def delete_scenario(s_id: int):
    pass
