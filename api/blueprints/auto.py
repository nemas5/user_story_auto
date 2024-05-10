import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for

blueprint_auto = Blueprint('bp_auto', __name__)

