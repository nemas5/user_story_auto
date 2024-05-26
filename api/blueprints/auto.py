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
        # print(login, password)
        user = get_admin(login, password, db_session)
        # print(user, 1)
        if user is None:
            user = get_common(login, password, db_session)
            # print(user, 2)
            if user is None:
                return make_response(jsonify({"ad": 0}), 201)
            session['user_id'] = user[0]
            session['user_group'] = 'common'
            return make_response(jsonify({"ad": 0}), 200)
        else:
            session['user_id'] = user[0]
            session['user_group'] = 'admin'
            return make_response(jsonify({"ad": 1}), 200)



