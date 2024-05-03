import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_utilities.work_with_db import select_dict, insert_table
from db_utilities.sql_provider import SQLProvider


blueprint_auto = Blueprint('bp_auto', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auto.route('/auto', methods=['GET', 'POST'])
def auto():
    if request.method == 'GET':
        return render_template('auto.html')
    login = request.form.get('login')
    password = request.form.get('password')
    _sql = provider.get('auto.sql', login=login, password=password, user_table='internal_users')
    user = select_dict(current_app.config['db_config'], _sql)
    print(user)
    if user:
        user = user.pop()
        session['user_id'] = user['u_id']
        session['user_group'] = 'admin'
        return redirect(url_for('bp_update.admin_menu'))
    else:
        _sql = provider.get('auto.sql', login=login, password=password, user_table='external_users')
        user = select_dict(current_app.config['db_config'], _sql)
        if user:
            user = user.pop()
            session['user_id'] = user['u_id']
            session['user_group'] = 'external'
            return redirect('http://127.0.0.1:5001')
        else:
            return render_template('auto.html', err='Неверное имя пользователя или пароль.')


@blueprint_auto.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template('reg.html')

    login = request.form.get('login')
    _sql = provider.get('check_reg.sql', login=login, u_id=login)
    if select_dict(current_app.config['db_config'], _sql):
        return render_template('reg.html', err='Пользователь с таким логином уже существует!')
    password = request.form.get('password')
    user_name = request.form.get('nm')
    user_mail = request.form.get('sm')
    if login and password and user_mail and user_name:
        _sql = provider.get('reg.sql', login=login, password=password, nm=user_name, sm=user_mail)
        insert_table(current_app.config['db_config'], _sql)
        return redirect(url_for('bp_auto.auto'))
    return render_template('reg.html', err='Введены некорректные данные')


@blueprint_auto.route('/exit')
def ex():
    session.pop("user_id")
    session.pop("user_group")
    session.clear()
    return redirect('http://127.0.0.1:5001')
