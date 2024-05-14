import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for

from db.storage import get_admin, get_common
from db.connection import get_session

blueprint_create = Blueprint('sc_create', __name__)
db_session = get_session()



