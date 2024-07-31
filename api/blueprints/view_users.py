import os
from flask import Blueprint,  request, jsonify, session, make_response

from db.storage import get_all_common, delete_user, prom_user
from db.connection import get_session

blueprint_users = Blueprint('bp_user', __name__)


@blueprint_users.route('/', methods=['GET'])
def view_users():
    db_session = get_session()
    users = get_all_common(db_session)
    res = [{'id': i[0], 'role': i[1]} for i in users]
    print(res)
    return make_response(jsonify(res), 200)


@blueprint_users.route('/del/<u_id>', methods=['DELETE'])
def del_user(u_id: str):
    db_session = get_session()
    delete_user(u_id, db_session)
    return make_response('', 200)


@blueprint_users.route('/prom/<u_id>', methods=['POST'])
def promote_user(u_id: str):
    db_session = get_session()
    prom_user(u_id, db_session)
    return make_response(jsonify({'id': u_id, 'role': 'admin'}), 200)
