import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for

from db.storage import get_all_common
from db.connection import get_session

blueprint_users = Blueprint('bp_user', __name__)
db_session = get_session()


@blueprint_users.route('/', methods=['GET'])
def view_users():
    users = get_all_common(db_session)
    return users

