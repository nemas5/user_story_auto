import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for

from db.storage import get_admin, get_common
from db.connection import get_session

blueprint_auto = Blueprint('bp_auto', __name__)
db_session = get_session()


@blueprint_auto.route('/auto', methods=['GET', 'POST'])
def auto():
    if request.method == 'GET':
        login = request.form.get('login')
        password = request.form.get('password')
        user = get_admin(login, password, db_session)
        if user is None:
            user = get_common(login, password, db_session)
            if user is None:
                return {"response": "0"}
            session['user_group'] = 'common'
        else:
            session['user_group'] = 'admin'
        session['user_id'] = user
        return {"response": "1"}

