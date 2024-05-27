import os
from flask import Blueprint, send_file,session, jsonify, make_response, request

from db.storage import get_admin, get_common
from db.connection import get_session

blueprint_download = Blueprint('bp_down', __name__)
db_session = get_session()


@blueprint_download.route('/download', methods=['POST'])
def download():
    file = request.json['file']
    return send_file(f'data_files/user_data/{session["user_id"]}/{file}.docx')
