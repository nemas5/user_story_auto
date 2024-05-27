import json

from flask import Flask
# from flask_cors import CORS
import docx

from api.blueprints import list_of_blueprints
from config import get_api_settings

from utilities.scenarios import Scenario


settings = get_api_settings()


def reg_blueprints(application: Flask) -> None:
    for bp, url_prefix in list_of_blueprints:
        application.register_blueprint(bp, url_prefix=url_prefix)


def get_app() -> Flask:
    application = Flask(__name__)
    reg_blueprints(application)
    return application


app = get_app()
# CORS(app)
app.secret_key = 'key'
with open('data_files/access.json') as file:
    app.config['access_config'] = json.load(file)

app.secret_key = 'key'

if __name__ == '__main__':
    app.run(host=settings.host, port=int(settings.port), debug=True)

