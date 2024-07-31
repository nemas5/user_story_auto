import os
from flask import Blueprint, render_template, request, current_app, session, jsonify, make_response

from db.storage import get_admin, get_common
from db.connection import get_session

blueprint_auto = Blueprint('bp_auto', __name__)
db_session = get_session()


@blueprint_auto.route('/auto', methods=['POST'])
def auto():
    if request.method == 'POST':

        login = request.json['login']
        password = request.json['password']
        user = get_common(login, password, db_session)
        if user is None:
            return make_response(jsonify({"ad": 0}), 201)
        session['user_id'] = user[0]
        session['user_group'] = user[1]
        if user[1] == 'admin':
            rights = 1
        else:
            rights = 0
        return make_response(jsonify({"ad": rights}), 200)




