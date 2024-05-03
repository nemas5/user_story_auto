import json
import os

from flask import Flask, render_template, session


app = Flask(__name__)
with open('data_files/db_config.json') as file:
    app.config['db_config'] = json.load(file)
with open('data_files/access.json') as file:
    app.config['access_config'] = json.load(file)
with open('data_files/reports.json', encoding='utf-8') as file:
    app.config['reports_config'] = json.load(file)
with open('data_files/query.json', encoding='utf-8') as file:
    app.config['query_config'] = json.load(file)
with open('data_files/cache.json') as f:
    app.config['cache_config'] = json.load(f)
app.register_blueprint(blueprint_auto, url_prefix='/auto')
app.register_blueprint(blueprint_film, url_prefix='/film')
app.register_blueprint(blueprint_session, url_prefix='/session')
app.register_blueprint(blueprint_schedule, url_prefix='/schedule')
app.register_blueprint(blueprint_update, url_prefix='/update')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_query, url_prefix='/query')
app.secret_key = 'key'

# provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@app.route('/', methods=['GET'])
def main_menu():
    return render_template('main_menu.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
