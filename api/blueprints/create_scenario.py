import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for

from db.storage import get_admin, get_common
from db.connection import get_session
from utilities.scenarios import Scenario

blueprint_create = Blueprint('sc_create', __name__)
db_session = get_session()


@blueprint_create.route('/', methods=['GET'])
def create_scenario():
    user = session["user_id"]
    scenario = Scenario()
    return Scenario


@blueprint_create.route('/save', methods=['GET'])
def save_scenario():
    pass
